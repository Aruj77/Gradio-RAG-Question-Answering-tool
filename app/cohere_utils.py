import cohere
import os
from dotenv import load_dotenv

load_dotenv()

COHERE_API_KEY = os.getenv("COHERE_API_KEY")

cohere_client = cohere.Client(api_key=COHERE_API_KEY)


def generate_answer(query, retrieved_docs):
    context = " ".join(retrieved_docs)
    prompt = f"Context: {context}\nQuestion: {query}\nAnswer:"
    response = cohere_client.generate(model="xlarge", prompt=prompt, max_tokens=100)
    return response.generations[0].text.strip()
