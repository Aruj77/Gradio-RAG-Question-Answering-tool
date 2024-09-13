import os
from dotenv import load_dotenv
from pinecone import Pinecone, ServerlessSpec
from app.embedding_utils import get_embedding

# Load environment variables from .env file
load_dotenv()

# Get the Pinecone API key from environment variables
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")

# Initialize Pinecone
pc = Pinecone(api_key=PINECONE_API_KEY)

# Check if index exists
if "qa-bot-index" in pc.list_indexes().names():
    # Delete the existing index if it exists
    pc.delete_index(name="qa-bot-index")

# Create a new index with the correct dimension
pc.create_index(
    name="qa-bot-index",
    dimension=384,  # Set this to the correct dimension
    metric="euclidean",
    spec=ServerlessSpec(cloud="aws", region="us-east-1"),
)

index = pc.Index("qa-bot-index")
