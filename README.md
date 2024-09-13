# QA Bot with Retrieval-Augmented Generation (RAG)

## Overview

This project implements a Retrieval-Augmented Generation (RAG) model to build a Question Answering (QA) bot. The bot can process uploaded PDF documents, generate embeddings for the content, and answer questions based on the document's content. The application uses Gradio for a user-friendly interface, Pinecone for vector storage and retrieval, and Cohere for generating answers.

## Features

- **Upload PDF Documents**: Users can upload PDF files containing relevant information.
- **Ask Questions**: Users can query the QA bot with questions related to the content of the uploaded documents.
- **Retrieve and Answer**: The bot retrieves relevant sections from the document and generates coherent answers.

## Folder Structure

```
project-root/
│
├── app/
│   ├── __init__.py
│   ├── pdf_utils.py
│   ├── pinecone_utils.py
│   ├── cohere_utils.py
│
├── requirements.txt
├── app.py
├── README.md
└── .env
```

## Prerequisites

- Python 3.7 or higher
- `pip` for installing dependencies

## Installation

1. **Clone the Repository**

   ```bash
   git clone https://github.com/yourusername/your-repo.git
   cd your-repo
   ```

2. **Set Up Virtual Environment**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Create `.env` File**

   Create a file named `.env` in the root directory and add your API keys:

   ```env
   PINECONE_API_KEY=your_pinecone_api_key
   COHERE_API_KEY=your_cohere_api_key
   ```

## Usage

1. **Run the Application**

   Start the Gradio interface:

   ```bash
   python app.py
   ```

   This will start a local server. You will see a public URL where you can access the web app.

2. **Interacting with the Web App**

   - **Upload PDF**: Click on "Upload PDF" to upload your document.
   - **Ask a Question**: Enter your question in the provided textbox.
   - **Get Answer**: Click the submit button to get an answer based on the content of the uploaded document.

## Files

- **`app.py`**: The main script to run the Gradio interface.
- **`app/pdf_utils.py`**: Functions for extracting text from PDF files.
- **`app/pinecone_utils.py`**: Functions for interacting with Pinecone (storing and retrieving document embeddings).
- **`app/cohere_utils.py`**: Functions for generating answers using the Cohere API.
- **`.env`**: Environment file for storing API keys.

## Troubleshooting

- **Vector Dimension Mismatch Error**:
  Ensure that the dimension of the vectors used in the Pinecone index matches the dimension of the embeddings. Update the `dimension` parameter when creating the Pinecone index.

- **API Key Issues**:
  Ensure that your API keys are correctly set in the `.env` file and that they have the necessary permissions.

- **Deprecation Warnings**:
  These warnings are related to future updates in the libraries. They do not usually affect the current functionality but be aware of them for future updates.

## Contributing

If you find issues or have suggestions for improvements, please feel free to open an issue or submit a pull request.
