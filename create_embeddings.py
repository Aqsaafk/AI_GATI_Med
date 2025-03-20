import os
from dotenv import load_dotenv 
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import AzureOpenAIEmbeddings  # ✅ Correct import
from langchain_community.vectorstores import FAISS

load_dotenv()

#Set up Azure OpenAI 
endpoint = os.getenv("ENDPOINT_URL", "https://oai-assistantapi-poc.openai.azure.com/")   
subscription_key = os.getenv("AZURE_OPENAI_API_KEY")

# ✅ Path to PDFs & Vector Store
PDF_FOLDER = "/mnt/d/My Folder/Hackathons/AI-GATI/Asthma_Literature"
VECTOR_STORE_PATH = "pdf_faiss_index"

# ✅ Load PDFs
documents = []
for pdf_file in os.listdir(PDF_FOLDER):
    if pdf_file.endswith(".pdf"):
        pdf_path = os.path.join(PDF_FOLDER, pdf_file)
        loader = PyPDFLoader(pdf_path)
        documents.extend(loader.load())

print(f"Loaded {len(documents)} pages of text.")

# ✅ Split into smaller chunks
text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
docs = text_splitter.split_documents(documents)

print(f"Split into {len(docs)} chunks.")

# ✅ Initialize Azure OpenAI Embeddings (Fix: `azure_endpoint` instead of `openai_api_base`)
embeddings = AzureOpenAIEmbeddings(
    azure_endpoint=endpoint,
    api_key=subscription_key,
    api_version="2024-08-01-preview",
    model="text-embedding-ada-002"
)

# ✅ Store in FAISS
vector_db = FAISS.from_documents(docs, embeddings)
vector_db.save_local(VECTOR_STORE_PATH)

print(f"Embeddings stored in {VECTOR_STORE_PATH}")
