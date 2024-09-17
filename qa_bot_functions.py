import cohere
from sentence_transformers import SentenceTransformer
import pdfplumber
import os

# API keys and initialization
pinecone_api_key = "17fa6302-1d73-4546-945f-8a8900066198"
cohere_api_key = "Tz1QAyJD5aIwdga6CJAxxjXCkp7cLdY1p9ZN3NC5"

# Initialize Cohere
co = cohere.Client(cohere_api_key)

# Initialize Pinecone
from pinecone import Pinecone, ServerlessSpec

pc = Pinecone(api_key=pinecone_api_key)

# Initialize Sentence Transformer model
model = SentenceTransformer("all-MiniLM-L6-v2")


# Extract text from PDF
def extract_text_from_pdf(pdf_path):
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text()
    return text


# Split text into chunks
def chunk_text(text, chunk_size=500):
    sentences = text.split(".")
    chunks = [
        " ".join(sentences[i : i + chunk_size])
        for i in range(0, len(sentences), chunk_size)
    ]
    return chunks


# Generate embeddings for text chunks
def generate_embeddings(chunks):
    embeddings = model.encode(chunks)
    return embeddings


# Set up Pinecone index
def setup_pinecone_index(embeddings, chunks, index_name):
    # Create Pinecone index if it does not exist
    if index_name not in pc.list_indexes().names():
        pc.create_index(
            name=index_name,
            dimension=len(embeddings[0]),  # Ensure this matches the embedding size
            metric="cosine",  # or "euclidean"
            spec=ServerlessSpec(cloud="aws", region="us-east-1"),
        )

    index = pc.Index(index_name)

    ids = [str(i) for i in range(len(embeddings))]
    vectors_to_upsert = [
        {
            "id": ids[i],
            "values": embeddings[i].tolist(),
            "metadata": {"text": chunks[i]},
        }
        for i in range(len(embeddings))
    ]
    index.upsert(vectors=vectors_to_upsert)

    return index


# Retrieve relevant chunks based on query
def retrieve_relevant_chunks(query, index, top_k=3):
    query_embedding = model.encode([query])[0]
    results = index.query(
        vector=query_embedding.tolist(), top_k=top_k, include_metadata=True
    )
    return [match["metadata"]["text"] for match in results["matches"]]


# Generate an answer using Cohere
def generate_answer(retrieved_chunks, question):
    context = " ".join(retrieved_chunks)
    prompt = f"Context: {context}\n\nQuestion: {question}\nAnswer:"
    response = co.generate(
        model="command", prompt=prompt, max_tokens=50, temperature=0.5
    )
    return response.generations[0].text.strip()


# Answer a question
def answer_question(question, index):
    # Retrieve relevant chunks
    retrieved_chunks = retrieve_relevant_chunks(question, index)

    if not retrieved_chunks:
        return "No relevant information found in the document."

    # Generate the answer
    return generate_answer(retrieved_chunks, question)


# Process a new PDF file and set up the index
def process_pdf(pdf_file):
    text = extract_text_from_pdf(
        pdf_file.name
    )  # Use pdf_file.name to get the path of the uploaded file
    chunks = chunk_text(text)
    embeddings = generate_embeddings(chunks)

    index_name = "qa-bot"
    index = setup_pinecone_index(embeddings, chunks, index_name)

    return index
