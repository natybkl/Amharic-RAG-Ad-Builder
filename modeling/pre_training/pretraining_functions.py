import os
import torch
from datasets import load_dataset
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    BitsAndBytesConfig,
    TrainingArguments,
    pipeline,
    logging,
)
from peft import LoraConfig
from trl import SFTTrainer

def load_dataset_from_files(data_files):
    return load_dataset('text', data_files=data_files)

def load_llama_model(base_model, quant_config):
    model = AutoModelForCausalLM.from_pretrained(
        base_model,
        quantization_config=quant_config,
        device_map={"": 0}
    )
    model.config.use_cache = False
    model.config.pretraining_tp = 1
    return model

def load_llama_tokenizer(tokenizer_name):
    tokenizer = AutoTokenizer.from_pretrained(tokenizer_name, use_auth_token=True)
    tokenizer.pad_token = tokenizer.eos_token
    tokenizer.padding_side = "right"
    return tokenizer

def train_llama_model(model, dataset, tokenizer, peft_params, training_params):
    trainer = SFTTrainer(
        model=model,
        train_dataset=dataset,
        peft_config=peft_params,
        dataset_text_field="text",
        max_seq_length=None,
        tokenizer=tokenizer,
        args=training_params,
        packing=False,
    )
    trainer.train()
    return trainer

def save_model_and_tokenizer(trainer, output_dir):
    trainer.model.save_pretrained(output_dir)
    trainer.tokenizer.save_pretrained(output_dir)
    logging.set_verbosity(logging.CRITICAL)

def generate_text_prompt(model, tokenizer, prompt):
    pipe = pipeline(task="text-generation", model=model, tokenizer=tokenizer, max_length=200)
    result = pipe(f"<s>[INST] {prompt} [/INST]")
    return result[0]['generated_text']