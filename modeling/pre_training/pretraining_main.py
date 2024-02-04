import os
from llama_pretraining import (
    load_dataset_from_files,
    load_llama_model,
    load_llama_tokenizer,
    train_llama_model,
    save_model_and_tokenizer,
    generate_text_prompt,
)
from transformers import BitsAndBytesConfig, TrainingArguments
from peft import LoraConfig

model_directory = "meta-llama/Llama-2-7b-hf"
base_model = model_directory

dataset_files = {'train': '/data/raw/CACO_TEXT.txt'}

compute_dtype = getattr(torch, "float16")
quant_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=compute_dtype,
    bnb_4bit_use_double_quant=False,
)

model = load_llama_model(base_model, quant_config)

tokenizer_name = "iocuydi/llama-2-amharic-3784m"
tokenizer = load_llama_tokenizer(tokenizer_name)

dataset = load_dataset_from_files(dataset_files)

peft_params = LoraConfig(
    lora_alpha=16,
    lora_dropout=0.1,
    r=64,
    bias="none",
    task_type="CAUSAL_LM",
)

training_params = TrainingArguments(
    output_dir="./results",
    num_train_epochs=1,
    per_device_train_batch_size=4,
    gradient_accumulation_steps=1,
    optim="paged_adamw_32bit",
    save_steps=1,
    logging_steps=1,
    learning_rate=2e-4,
    weight_decay=0.001,
    fp16=False,
    bf16=False,
    max_grad_norm=0.3,
    max_steps=20,
    warmup_ratio=0.03,
    group_by_length=True,
    lr_scheduler_type="constant",
    report_to="wandb"
)

trainer = train_llama_model(model, dataset, tokenizer, peft_params, training_params)

new_model = "llama-2-7b-chat-amharic"
save_model_and_tokenizer(trainer, new_model)

prompt = "ኢትዮጵያ የት ምትግኝ ሀገር ናት?"
generated_text = generate_text_prompt(model, tokenizer, prompt)
print(generated_text)