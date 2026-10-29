import torch
from datasets import load_dataset
from transformers import (
    AutoTokenizer,
    AutoModelForSeq2SeqLM,
    TrainingArguments,
    Trainer,
    DataCollatorForSeq2Seq,
)
from peft import LoraConfig, get_peft_model


# --------------------------------------------------
# 1. Configuration
# --------------------------------------------------

MODEL_NAME = "google/flan-t5-base"

OUTPUT_DIR = "./math_tutor"

MAX_INPUT_LENGTH = 256
MAX_TARGET_LENGTH = 256


# --------------------------------------------------
# 2. Load GSM8K
# --------------------------------------------------

print("Loading GSM8K...")

dataset = load_dataset(
    "openai/gsm8k",
    "main"
)

train_data = dataset["train"]
test_data = dataset["test"]

print("Training examples:", len(train_data))
print("Test examples:", len(test_data))


# --------------------------------------------------
# 3. Tokenizer
# --------------------------------------------------

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)


# --------------------------------------------------
# 4. Convert GSM8K → instruction/answer format
# --------------------------------------------------

def preprocess(example):

    question = example["question"]
    answer = example["answer"]

    prompt = f"""
You are a patient mathematics tutor.

Solve this math word problem step by step.
Explain the reasoning clearly and give the final answer.

Problem:
{question}

Solution:
"""

    model_inputs = tokenizer(
        prompt,
        max_length=MAX_INPUT_LENGTH,
        truncation=True,
    )

    labels = tokenizer(
        answer,
        max_length=MAX_TARGET_LENGTH,
        truncation=True,
    )

    model_inputs["labels"] = labels["input_ids"]

    return model_inputs


print("Tokenizing dataset...")

tokenized_train = train_data.map(
    preprocess,
    remove_columns=train_data.column_names
)

tokenized_test = test_data.map(
    preprocess,
    remove_columns=test_data.column_names
)


# --------------------------------------------------
# 5. Load pretrained model
# --------------------------------------------------

print("Loading model...")

model = AutoModelForSeq2SeqLM.from_pretrained(
    MODEL_NAME
)


# --------------------------------------------------
# 6. LoRA configuration
# --------------------------------------------------

lora_config = LoraConfig(
    r=8,
    lora_alpha=16,
    target_modules=["q", "v"],
    lora_dropout=0.05,
    bias="none",
    task_type="SEQ_2_SEQ_LM",
)

model = get_peft_model(
    model,
    lora_config
)

model.print_trainable_parameters()


# --------------------------------------------------
# 7. Training configuration
# --------------------------------------------------

training_args = TrainingArguments(
    output_dir=OUTPUT_DIR,

    num_train_epochs=1,

    per_device_train_batch_size=4,
    per_device_eval_batch_size=4,

    gradient_accumulation_steps=4,

    learning_rate=2e-4,

    logging_steps=100,

    eval_strategy="steps",
    eval_steps=500,

    save_steps=500,
    save_total_limit=2,

    fp16=torch.cuda.is_available(),

    report_to="none",
)


# --------------------------------------------------
# 8. Data collator
# --------------------------------------------------

data_collator = DataCollatorForSeq2Seq(
    tokenizer=tokenizer,
    model=model,
)


# --------------------------------------------------
# 9. Trainer
# --------------------------------------------------

trainer = Trainer(
    model=model,
    args=training_args,

    train_dataset=tokenized_train,
    eval_dataset=tokenized_test,

    tokenizer=tokenizer,
    data_collator=data_collator,
)


# --------------------------------------------------
# 10. Train
# --------------------------------------------------

print("\nStarting fine-tuning...\n")

trainer.train()


# --------------------------------------------------
# 11. Save
# --------------------------------------------------

print("\nSaving model...")

model.save_pretrained(OUTPUT_DIR)
tokenizer.save_pretrained(OUTPUT_DIR)

print("\nDone!")
print("Model saved to:", OUTPUT_DIR)