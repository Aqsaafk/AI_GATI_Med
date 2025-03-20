from dotenv import load_dotenv 
import os 
from langchain_community.vectorstores import FAISS
from langchain_openai import AzureOpenAIEmbeddings

load_dotenv()

#Set up Azure OpenAI 
endpoint = os.getenv("ENDPOINT_URL", "https://oai-assistantapi-poc.openai.azure.com/")   
subscription_key = os.getenv("AZURE_OPENAI_API_KEY")

# Initialize AzureOpenAIEmbeddings with correct parameters
embeddings = AzureOpenAIEmbeddings(
    azure_endpoint=endpoint,
    api_key=subscription_key,
    azure_deployment="text-embedding-ada-002",
    api_version="2023-07-01-preview" 
)

# Load FAISS index
# Load FAISS index with safe deserialization
vector_db = FAISS.load_local("pdf_faiss_index", embeddings, allow_dangerous_deserialization=True)

print("Embeddings loaded successfully!")

query = "My mother (or anyone) is experiencing breathing issues. Could it be asthma?"  # Replace with your test query
results = vector_db.similarity_search(query, k=3)  # Retrieve top 3 relevant chunks

for i, doc in enumerate(results):
    print(f"Result {i+1}:")
    print(doc.page_content)
    print("-" * 50)

