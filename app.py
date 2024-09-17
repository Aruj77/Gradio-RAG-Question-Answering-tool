import gradio as gr
from qa_bot_functions import process_pdf, answer_question


def gradio_interface(pdf_file, question):
    if pdf_file is not None:
        index = process_pdf(pdf_file)
        answer = answer_question(question, index)
        return answer
    else:
        return "Please upload a PDF file."


# Create Gradio interface
iface = gr.Interface(
    fn=gradio_interface,
    inputs=[
        gr.File(label="Upload PDF"),  # Updated way to handle file inputs
        gr.Textbox(label="Ask a Question"),  # Input for questions
    ],
    outputs=gr.Textbox(label="Answer"),  # Output for the answer
)

# Launch Gradio interface
if __name__ == "__main__":
    iface.launch()
