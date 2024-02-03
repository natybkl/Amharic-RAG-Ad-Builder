import os
import torch
from llama_functions import load_model, create_bnb_config, preprocess_dataset, train

# Define your constants or configurations here

# Load model and tokenizer
model_name = "meta-llama/Llama-2-7b-hf"
bnb_config = create_bnb_config()
model, tokenizer = load_model(model_name, bnb_config)

seed = 42

dataset = "/home/mistral/data/new_cleaned/G3_All_Data_All.csv"
dataset = preprocess_dataset(tokenizer, seed, dataset)

# Train the model
output_dir = "results"
train(model, tokenizer, dataset, output_dir)