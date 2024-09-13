from app.pinecone_utils import retrieve_relevant_docs
from app.cohere_utils import generate_answer


def rag_qa(query):
    retrieved_docs = retrieve_relevant_docs(query)
    answer = generate_answer(query, retrieved_docs)
    return answer
