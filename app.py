from langchain_openai import AzureChatOpenAI
from langchain.tools import Tool
from dotenv import load_dotenv 
import os 
import requests
from langchain.agents import create_openai_tools_agent, AgentExecutor
from langchain.memory import ConversationBufferMemory
from langchain.agents import initialize_agent, AgentType


#load environment variables 
load_dotenv()

#Set up Azure OpenAI 
endpoint = os.getenv("ENDPOINT_URL", "<YOUR_ENDPOINT_URL>")  
deployment = os.getenv("DEPLOYMENT_NAME", "gpt-4o")  
subscription_key = os.getenv("AZURE_OPENAI_API_KEY")

#API KEYS
google_api_key = os.getenv("GOOGLE_API_KEY")


#Initialize_LLM
llm = AzureChatOpenAI(
    azure_endpoint=endpoint,
    azure_deployment=deployment,
    api_key=subscription_key,
    api_version="2024-08-01-preview",
    )


def get_geolocation(city: str = None) -> dict:
    """Fetch geolocation using Google API based on city name or IP."""
    if city:
        print(f"Fetching coordinates for {city}...")
        url = f"https://maps.googleapis.com/maps/api/geocode/json?address={city}&key={google_api_key}"
        response = requests.get(url)
        if response.status_code == 200:
            results = response.json().get("results", [])
            if results:
                location = results[0]["geometry"]["location"]
                return {"lat": location["lat"], "lng": location["lng"]}
        return {"error": f"Failed to fetch geolocation for {city}."}

    # If no city is provided, use IP-based geolocation
    print("Fetching geolocation based on IP...")
    url = f"https://www.googleapis.com/geolocation/v1/geolocate?key={google_api_key}"
    data = {"considerIp": True}
    headers = {"Content-Type": "application/json"}
    response = requests.post(url, json=data, headers=headers)
    
    return response.json().get("location", {}) if response.status_code == 200 else {"error": "Failed to fetch location"}

def get_air_quality(lat: float, lon: float) -> dict:
    """Fetch the air quality index for given latitude & longitude."""
    print(f"Fetching AQI for coordinates: {lat}, {lon}...")
    url = f"https://airquality.googleapis.com/v1/currentConditions:lookup?key={google_api_key}"
    data = {"location": {"latitude": lat, "longitude": lon}}
    headers = {"Content-Type": "application/json"}

    response = requests.post(url, json=data, headers=headers)
    raw_data = response.json()

    # Extract required fields correctly
    if "indexes" in raw_data and isinstance(raw_data["indexes"], list) and raw_data["indexes"]:
        aqi_data = raw_data["indexes"][0]  # Assuming first index is the relevant one
        return {
            "aqi": aqi_data.get("aqi", "Unknown"),
            "category": aqi_data.get("category", "Unknown"),
            "dominantPollutant": aqi_data.get("dominantPollutant", "Unknown")
        }

    return {"aqi": "Unknown", "category": "Unknown", "dominantPollutant": "Unknown"}


def get_air_quality_for_user(city: str = None) -> dict:
    """Fetch air quality based on the specified city or user's detected location."""
    print(f"Processing AQI request for city: {city}...")

    location = get_geolocation(city)
    if "error" in location:
        return {"error": "I couldn't determine your location. Please try specifying a valid city."}

    lat, lon = location.get("lat"), location.get("lng")
    
    air_quality = get_air_quality(lat, lon)

    aqi= air_quality.get("aqi", -1)
    category = air_quality.get("category", "Unknown")
    dominantPollutant = air_quality.get("dominantPollutant", "Unknown")

    # Structure the output, but allow LLM to interpret and respond naturally
    response = {
        "aqi": aqi,
        "category": category,
        "dominantPollutant": dominantPollutant,
        "city": city,
        "recommendation": f"The air quality in {city} is currently {category} (aqi: {aqi}). "
                          f"The dominant pollutant is {dominantPollutant}. "
                          "Based on this, what should be the best precautionary steps for I am an asthma patient?"
    }

    return response

# ✅ Define LangChain Tools
geolocation_tool = Tool(
    name="get_geolocation",
    func=get_geolocation,
    description="Fetches the user's geolocation.",
)

air_quality_tool = Tool(
    name="get_air_quality_for_user",
    func=get_air_quality_for_user,
    description="Fetches air quality index based on user's location.",
    return_direct=True  # ✅ Ensures function output is used directly
)

#Tools
tools=[geolocation_tool, air_quality_tool]
# Initialize the LangChain Agent
agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)
# Define the user query
user_query = "What is the AQI of Capetown"

# Run the agent
struct_response = agent.run(user_query)
print(struct_response)

#Follow up 
def format_air_quality(data):
    return (f"The air quality in {data['city']} is currently {data['category']} (AQI: {data['aqi']}). "
            f"The dominant pollutant is {data['dominantPollutant']}. "
            f"Recommendation: {data['recommendation']}")

response=format_air_quality(struct_response)

#Re-run the agent 
final_response=agent.run(response)
print(final_response)





