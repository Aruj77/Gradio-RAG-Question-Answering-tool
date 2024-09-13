import gradio as gr
import os
from transformers import pipeline
from app.pdf_utils import extract_text_from_pdf
from app.pinecone_utils import store_pdf_embeddings
from app.qa_bot import rag_qa

# Example of using a simple question-answering model
qa_model = pipeline("question-answering")


def process_pdf(pdf_file):
    try:
        text = extract_text_from_pdf(pdf_file)
        message = store_pdf_embeddings(text, pdf_file.name)
        return message
    except Exception as e:
        return f"Error processing PDF: {e}"


def get_answer(query):
    try:
        # This is where you'd integrate your RAG model
        answer = qa_model(question=query, context="Sample context text")
        return answer["answer"]
    except Exception as e:
        return f"Error generating answer: {e}"


def qa_bot_interface(pdf_file, query):
    if pdf_file:
        result = process_pdf(pdf_file)
    if query:
        answer = get_answer(query)
    return result, answer


iface = gr.Interface(
    fn=qa_bot_interface,
    inputs=[
        gr.File(label="Upload PDF"),
        gr.Textbox(label="Ask a Question", placeholder="Type your question here..."),
    ],
    outputs=["text", "text"],
    title="QA Bot with Document Upload",
    description="Upload a PDF and ask questions related to the document.",
)

if __name__ == "__main__":
    iface.launch(share=True)
