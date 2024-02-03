import json
import os

from langchain.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter  
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema.runnable import RunnablePassthrough
from langchain.schema.output_parser import StrOutputParser
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Weaviate
from transformers import AutoModelForCausalLM, AutoTokenizer, GenerationConfig, pipeline, BitsAndBytesConfig, AutoModelForSeq2SeqLM
# import torch
from langchain_community.embeddings import HuggingFaceEmbeddings
from datasets import Dataset
import random
from tools import too

from langchain.agents import AgentType, initialize_agent
from langchain.schema import SystemMessage

import weaviate
from dotenv import load_dotenv,find_dotenv
from weaviate.embedded import EmbeddedOptions

from langchain import HuggingFacePipeline

with open("system_message.txt", "r") as file:
    system_message = file.read()


# Load OpenAI API key from .env file
load_dotenv(find_dotenv())


def data_loader(file_path= '../prompts/challenge_doc.txt', chunk_size=500, chunk_overlap=50):
    try:
        loader = TextLoader(file_path)
        documents = loader.load()

        # Chunk the data
        text_splitter = CharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
        chunks = text_splitter.split_documents(documents)
        
        print("data loaded to vector database successfully")
        return chunks
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None 


def create_chunks(documents, chunk_size=500, chunk_overlap=50):
    try:
        # Chunk the data
        text_splitter = CharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)

        chunks = text_splitter.split_documents(documents)
        
        print("data loaded to vector database successfully")
        return chunks
    except Exception as e:
        
        print(f"An unexpected error occurred: {e}")
        return None 


def create_langchain_pipeline(retriever, template, temperature=0):
    try:
        # Define LLM
        llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=temperature)

        # Define prompt template
        
        prompt = ChatPromptTemplate.from_template(template)

        # Setup RAG pipeline
        rag_chain = (
            {"context": retriever,  "question": RunnablePassthrough()} 
            | prompt 
            | llm
            | StrOutputParser() 
        )

        print("langchain with rag pipeline created successfully.")
        return rag_chain

    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None 


def create_retriever(chunks, embeddings):
    try:
        
        # Load OpenAI API key from .env file
        load_dotenv(find_dotenv())


        # Setup vector database
        client = weaviate.Client(
            embedded_options = EmbeddedOptions()
        )

        # Populate vector database
        vectorstore = Weaviate.from_documents(
            client = client,    
            documents = chunks,
            embedding =  OpenAIEmbeddings(),
            by_text = False
        )

        # Define vectorstore as retriever to enable semantic search
        retriever = vectorstore.as_retriever()
        print("create retriver  succesfully.")

        return retriever
    
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None 
    


def load_file(file_path):
    try:

        # Open the file in read mode
        with open(file_path, 'r') as file:
            # Read the contents of the file
            file_contents = file.read()   
        
        return file_contents
        
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None 


def load_model(model_name, bnb_config):
    try:
        n_gpus = torch.cuda.device_count()
        max_memory = f'{23000}MB'

        #method from the Hugging Face Transformers library to load a pre-trained language model
        model = AutoModelForCausalLM.from_pretrained(
            model_name,
            quantization_config=bnb_config,
            device_map="auto", # dispatch efficiently the model on the available ressources
            max_memory = {i: max_memory for i in range(n_gpus)},
        )
        tokenizer = AutoTokenizer.from_pretrained(model_name, use_auth_token=True)

        # Needed for LLaMA tokenizer
        tokenizer.pad_token = tokenizer.eos_token
        print("load the model successfully")
        return model, tokenizer
    
    except Exception as e:
        print(f"An unexpected error occurred loading model: {e}")
        return None 

def create_bnb_config():
    try:
        bnb_config = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_use_double_quant=True,
            bnb_4bit_quant_type="nf4",
            bnb_4bit_compute_dtype=torch.bfloat16,
        )
        print("creae bnb config success.")
        return bnb_config
     
    except Exception as e:
        print(f"An unexpected error occurred while creating bnb config: {e}")
        return None 


def create_huggingface_embeeding(model_name="sentence-transformers/all-mpnet-base-v2"):
    try:
        model_kwargs = {}
        embeddings = HuggingFaceEmbeddings(
        model_name=model_name, 
        model_kwargs=model_kwargs
        )
        print("create huggingface embeeding successfully")
        return embeddings
    
    except Exception as e:
        print(f"An unexpected error occurred while creating bnb config: {e}")
        return None 
    
def create_huggingface_llm(model_name="meta-llama/Llama-2-7b-hf"):
    try:
        bnb_config = create_bnb_config()
        model, tokenizer = load_model(model_name, bnb_config)

        llm_pipeline = pipeline(
        "text-generation",
        model=model,
        tokenizer=tokenizer,
        use_cache=True,
        device_map="auto",
        max_length=2048,
        do_sample=True,
        top_k=5,
        num_return_sequences=1,
        eos_token_id=tokenizer.eos_token_id,
        pad_token_id=tokenizer.eos_token_id,
    )

        # specify the llm
        llm = HuggingFacePipeline(pipeline=llm_pipeline)

        return llm
    
    except Exception as e:
        print(f"An unexpected error occurred while creating bnb config: {e}")
        return None 
    

def get_agent_executor(selected_model, retriever, temperature=0):

    try:
        llm = ChatOpenAI(model_name=selected_model, temperature=temperature)

        # Define prompt template
        prompt = ChatPromptTemplate.from_template(system_message)

        # Setup RAG pipeline
        rag_chain = (
            {"context": retriever,  "question": RunnablePassthrough()} 
            | prompt 
            | llm
            | StrOutputParser() 
        )

        print("langchain with rag pipeline created successfully.")

        return rag_chain
    
    except Exception as e:
        print(f"An unexpected error occurred while creating bnb config: {e}")
        return None 
    


    # analyst_agent = initialize_agent(
    #     llm=ChatOpenAI(temperature=0.1, model = selected_model),
    #     tools=[too],
    #     agent_kwargs=agent_kwargs,
    #     verbose=True,
    #     max_iterations=20,
    #     early_stopping_method='generate'
    # )

    # return analyst_agent