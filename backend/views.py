from flask import Blueprint, jsonify, request
import json
import logging
from langchain.chat_models import ChatOpenAI
from langchain.embeddings import OpenAIEmbeddings

from PyPDF2 import PdfReader  # Use PdfReader instead of PdfFileReader
import re
from langchain.docstore.document import Document
import os
from rag_utils import create_retriever, data_loader, create_chunks, create_huggingface_embeeding, get_agent_executor

main_bp = Blueprint('main', __name__)
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
uploaded_files = []
chunks = []

openai_embeddings = OpenAIEmbeddings()
sentence_transformer_embeedings = create_huggingface_embeeding()

openai_4_llm = ChatOpenAI(temperature=0.1, model = 'gpt-4-1106-preview'),
openai_3_llm = ChatOpenAI(temperature=0.1, model = 'gpt-3.5-turbo'),

model_pairs = {
        "gpt-4-1106-preview": openai_4_llm,
        "gpt-3.5-turbo": openai_3_llm
}

global selected_model, analyst_agent
selected_model = "gpt-4-1106-preview"

retriver = create_retriever(chunks, openai_embeddings)

analyst_agent = get_agent_executor(selected_model, retriver)

@main_bp.route('/api/v1/file-upload', methods=['POST'])
def upload_file():
    response = {
        "data": None,
        "error": None
    }
    statusCode = 404
    try:
        if 'file' not in request.files:
            raise ValueError("No file part")

        file = request.files['file']
    
        
        if file.filename == '':
            raise ValueError("No selected file")
    
        if not file.filename.endswith('.pdf'):
            raise ValueError("The selected file is not pdf. upload only pdf file")

         # Check if the file is a PDF
        if file.filename.endswith('.pdf'):
            pdf_reader = PdfReader(file)
            num_pages = len(pdf_reader.pages)  # Update to use len(pdf_reader.pages)

            text = ''
            # Extract text from each page
            for page_number in range(num_pages):
                page = pdf_reader.pages[page_number]
                text += page.extract_text()

            cleaned_text = re.sub(r'[^A-Za-z\s]', '', text)


              # Convert to lowercase
            cleaned_text = cleaned_text.lower()
            # Remove extra whitespaces
            cleaned_text = ' '.join(cleaned_text.split())
            file_path = os.path.join("uploads", file.filename)

            filename_without_extension = os.path.splitext(file_path)[0]
            filename_without_spaces = filename_without_extension.replace(" ", "")

            # Create the new file path with .txt extension
            new_file_path = filename_without_spaces + ".txt"

            print("file path: ", file_path)
            print("content: ", )

            with open(new_file_path, 'w') as file:
                file.write(cleaned_text)

            new_chuncks = data_loader(new_file_path)
          
            chunks.append(new_chuncks)
    
        response["data"] = str(chunks)
        statusCode = 200

    except Exception as error:
        logging.error(error)
        response['error'] = {
            'message': f"{error}"
        }
        statusCode = 404

    return jsonify(response), statusCode


@main_bp.route('/api/v1/chat', methods=['POST'])
def index():
    global selected_model, analyst_agent

    data = request.json
    response = {
        "data" : None,
        "error" : None
    }
    statusCode = 404
    try:
        logging.info(f"data: {data}")
        message = data['message']
        model_type = data["model_type"]
        selected_model = model_type
        print("selected modeL", selected_model, model_pairs[selected_model])

        retriver = create_retriever(chunks, openai_embeddings)
        print("retriver: ", type(retriver))

        analyst_agent = get_agent_executor(selected_model, retriver)

        print("agent anlyst: ", type(analyst_agent))

        answer = analyst_agent.invoke(message)

        logging.info(f"model:  {selected_model}, response: {answer}")

        response["data"] = answer
        statusCode = 200

    except Exception as error:
        logging.error(error)
        response['error'] = {
        'message': f"{error}"
        }
        statusCode = 404
    return jsonify(response), statusCode



@main_bp.route('/', methods=['GET'])
def base_get():
    response = {
        "data" : "The backend is working...",
        "error" : None
    }

    return jsonify(response), 200