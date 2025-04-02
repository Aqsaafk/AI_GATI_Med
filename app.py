from langchain_openai import AzureChatOpenAI
from langchain.tools import Tool
from dotenv import load_dotenv 
import os 
import requests
from langchain.prompts import PromptTemplate
from langchain.agents import initialize_agent, AgentType
from langchain_community.vectorstores import FAISS
from langchain_openai import AzureOpenAIEmbeddings
import json

#load environment variables 
load_dotenv()

#Set up Azure OpenAI 
endpoint = os.getenv("ENDPOINT_URL", "https://oai-assistantapi-poc.openai.azure.com/")  
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
    temperature=0.7,
    )

# Initialize AzureOpenAIEmbeddings with correct parameters
embeddings = AzureOpenAIEmbeddings(
    azure_endpoint=endpoint,
    api_key=subscription_key,
    azure_deployment="text-embedding-ada-002",
    api_version="2023-07-01-preview" 
)

# Load FAISS index with safe deserialization
vector_db = FAISS.load_local("pdf_faiss_index", embeddings, allow_dangerous_deserialization=True)

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

    return json.dumps({
        "city": city,
        "aqi": aqi,
        "category": category,
        "dominantPollutant": dominantPollutant
    })
    

def search_embeddings(query: str):
    """Retrieve relevant documents from FAISS vector database and enhance results using LLM."""
    
    # Step 1: Perform similarity search
    results = vector_db.similarity_search(query, k=3)
    retrieved_docs = [doc.page_content for doc in results] if results else []

    if not retrieved_docs:
        return "No relevant documents found."

    # Step 2: Enhance results using LLM
    prompt_template = PromptTemplate(
        input_variables=["query", "retrieved_docs"],
        template=(
            "You are BreathWell AI enhancing search results from vector embeddings. The user asked: '{query}'.\n\n"
            "Here are the retrieved documents:\n\n"
            "{retrieved_docs}\n\n"
            "Please analyze them and provide the most relevant, well-structured response. "
            "If possible, include key takeaways or insights."
            "But don't add any new information from your side"
        ),
    )

    # Generate enhanced response
    response = llm.invoke(prompt_template.format(query=query, retrieved_docs="\n".join(retrieved_docs)))

    return response.content if hasattr(response, "content") else "Error: Unable to generate response."

def get_aqi_recommendations(data) -> str:
    """Provide health recommendations based on AQI data."""
    if isinstance(data, str):  # If JSON string, convert to dictionary
        try:
            data = json.loads(data)
        except json.JSONDecodeError:
            return "Error: Invalid JSON format for AQI data."

    aqi = data.get("aqi")
    category = data.get("category")
    dominantPollutant = data.get("dominantPollutant")

    if aqi is None or category is None or dominantPollutant is None:
        return "Error: Missing required air quality data."

    # Structured prompt with controlled flexibility
    prompt_template = PromptTemplate(
        input_variables=["category", "aqi", "dominantPollutant"],
        template=(
            "You are a helpful AI BreathWell Assistant that provides air quality recommendations. "
            "The air quality category is '{category}', with an AQI of {aqi}. "
            "The dominant pollutant is {dominantPollutant}. "
            "\n\n"
            "Give a short but informative summary of what this air quality means. "
            "Provide actionable health recommendations, taking into account different levels of risk. "
            "For moderate air quality, keep a chill and casual tone, suggesting precautions in a friendly manner. "
            "For poor air quality, be very serious and recommend critical actions like PFT tests, emergency medicine, and protective measures. "
            "For good air quality, be very friendly, encouraging the user to enjoy their day while taking regular medicines. "
            "\n\n"
            "End with an uplifting and relevant inspirational quote. Do not repeat the same advice every time."
            "Use a lot of emojis"
        ),
    )
    

    # Generate response
    response = llm.invoke(prompt_template.format(category=category, aqi=aqi, dominantPollutant=dominantPollutant))

    return response.content if hasattr(response, "content") else "Error: Unable to generate response."

# ✅ Define LangChain Tools
geolocation_tool = Tool(
    name="get_geolocation",
    func=get_geolocation,
    description="Fetches the user's geolocation.",
)

air_quality_tool = Tool(
    name="get_air_quality_for_user",
    func=get_air_quality_for_user,
    description="Fetches air quality index based on user's location."
    "This information should be used to call GetAQIRecommendations next.",
     # ✅ Ensures function output is used directly
)

embedding_tooL=Tool(
    name="search_embeddings",
    func=search_embeddings,
    description="It goes through embeddings when needed according to the user query. Especially if the user has not provided geolocation"
    "n/ although user can mention city and some query which requires checking out all the tools and then giving out response",
    return_direct=True
)

aqi_recommendation_tool=Tool(
        name="GetAQIRecommendations",
        func=get_aqi_recommendations,
        description="Provides health recommendations based on aqi data. Requires aqi value, category, and dominant pollutant as inputs.",
        return_direct=True

    )

custom_prompt="You are called BreathWell AI, an asthma assistant. You have a patient's data in the form of embeddings. Accordingly you should give recommendations. Also sometimes, based on location and AQI." \
" Sometimes you just have retrieve patient information and present it in a presentable manner. Take care of your tasks. You are very empathetic" \
"Return the LLM's response as is, without modifications." \
"Use lots of emojis and friendly tone, write an inspirational quote in the end of your recommendation"

#Tools
tools=[geolocation_tool, air_quality_tool, embedding_tooL, aqi_recommendation_tool]
# Initialize the LangChain Agent
agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    agent_kwargs={"system_message": custom_prompt},
    verbose=True,
    handle_parsing_errors=True
)









