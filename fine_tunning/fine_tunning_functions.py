import torch
import os
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig, DataCollatorForLanguageModeling
from functools import partial
from peft import LoraConfig, get_peft_model

def load_model(model_name, bnb_config):
    n_gpus = torch.cuda.device_count()
    max_memory = f'{23000}MB'

    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        quantization_config=bnb_config,
        device_map="auto",
        max_memory={i: max_memory for i in range(n_gpus)},
    )

    tokenizer = AutoTokenizer.from_pretrained("keriii/KerodAmharicTokenizer3", use_auth_token=True)
    tokenizer.pad_token = tokenizer.eos_token

    return model, tokenizer

def create_bnb_config():
    bnb_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_use_double_quant=True,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_compute_dtype=torch.bfloat16,
    )

    return bnb_config

def create_peft_config(modules):
    config = LoraConfig(
        r=16,
        lora_alpha=64,
        target_modules=modules,
        lora_dropout=0.1,
        bias="none",
        task_type="CAUSAL_LM",
    )

    return config

def find_all_linear_names(model):
    cls = torch.nn.Linear
    lora_module_names = set()
    for name, module in model.named_modules():
        if isinstance(module, cls):
            names = name.split('.')
            lora_module_names.add(names[0] if len(names) == 1 else names[-1])

    if 'lm_head' in lora_module_names:
        lora_module_names.remove('lm_head')
    return list(lora_module_names)

def print_trainable_parameters(model, use_4bit=False):
    trainable_params = 0
    all_param = 0
    for _, param in model.named_parameters():
        num_params = param.numel()
        all_param += num_params
        if param.requires_grad:
            trainable_params += num_params
    if use_4bit:
        trainable_params /= 2
    print(
        f"all params: {all_param:,d} || trainable params: {trainable_params:,d} || trainable%: {100 * trainable_params / all_param}"
    )

def preprocess_batch(batch, tokenizer, max_length):
    return tokenizer(
        batch["text"],
        max_length=max_length,
        truncation=True,
    )

def create_prompt_formats(sample):
    """
    Format various fields of the sample ('text', 'label',)
    Then concatenate them using two newline characters
    :param sample: Sample dictionary
    """

    INTRO_BLURB = "Identify label from the given text."
    INSTRUCTION_KEY = "### Text:"
    RESPONSE_KEY = "label:"
    END_KEY = "### End"

    blurb = f"{INTRO_BLURB}"
    text = f"{INSTRUCTION_KEY}\n{sample['text']}"
    response = f"{RESPONSE_KEY}\n{sample['label']}"
    end = f"{END_KEY}"

    parts = [part for part in [blurb, text, response, end] if part]

    formatted_prompt = "\n\n".join(parts)

    sample["text"] = formatted_prompt

    return sample


def preprocess_dataset(tokenizer, seed, dataset):
    dataset = dataset.map(create_prompt_formats)
    _preprocessing_function = partial(preprocess_batch, tokenizer=tokenizer)  # Remove max_length argument
    dataset = dataset.map(
        _preprocessing_function,
        batched=True,
        remove_columns=["text", "label"],
    )
    dataset = dataset.shuffle(seed=seed)
    return dataset

def train(model, tokenizer, dataset, output_dir):
    model.gradient_checkpointing_enable()
    model = prepare_model_for_kbit_training(model)
    modules = find_all_linear_names(model)
    peft_config = create_peft_config(modules)
    model = get_peft_model(model, peft_config)
    print_trainable_parameters(model)
    trainer = Trainer(
        model=model,
        train_dataset=dataset,
        args=TrainingArguments(
            per_device_train_batch_size=1,
            gradient_accumulation_steps=4,
            warmup_steps=2,
            max_steps=50,
            learning_rate=2e-4,
            fp16=True,
            logging_steps=1,
            output_dir=output_dir,
            optim="paged_adamw_8bit",
            report_to=[]
        ),
        data_collator=DataCollatorForLanguageModeling(tokenizer, mlm=False)
    )
    model.config.use_cache = False
    do_train = True
    print("Training...")

    if do_train:
        train_result = trainer.train()
        metrics = train_result.metrics
        trainer.log_metrics("train", metrics)
        trainer.save_metrics("train", metrics)
        trainer.save_state()
        print(metrics)

    print("Saving last checkpoint of the model...")
    os.makedirs(output_dir, exist_ok=True)
    trainer.model.save_pretrained(output_dir)

    del model
    del trainer
    torch.cuda.empty_cache()