# SHARAD PANDEY
import os
import pandas as pd
from transformers import GPT2LMHeadModel, GPT2Tokenizer, Trainer, TrainingArguments, DataCollatorForLanguageModeling
from datasets import Dataset
import torch
# Load CSV file
file_path = r'C:\\Users\\shara\\CHATBOT\\Mental_Health_FAQ.csv'
df = pd.read_csv(file_path)

# Concatenate Questions and Answers into a single text column
df['text'] = df['Questions'] + " " + df['Answers']

# Convert DataFrame to Dataset
dataset = Dataset.from_pandas(df[['text']])

# Initialize tokenizer and model
tokenizer = GPT2Tokenizer.from_pretrained('gpt2')
tokenizer.pad_token = tokenizer.eos_token
model = GPT2LMHeadModel.from_pretrained('gpt2')

# Tokenize dataset
def tokenize_function(examples):
    return tokenizer(examples['text'], return_tensors='pt', max_length=128, truncation=True, padding='max_length')

tokenized_datasets = dataset.map(tokenize_function, batched=True, remove_columns=['text'])

# Data collator
data_collator = DataCollatorForLanguageModeling(tokenizer=tokenizer, mlm=False)

# Configuration for training # HYperparameter
training_args = TrainingArguments(
    output_dir="./results",
    overwrite_output_dir=True,
    num_train_epochs=1,
    per_device_train_batch_size=2,
    save_steps=10,
    save_total_limit=2,
)

# Initialize Trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_datasets,
    data_collator=data_collator,
)

# Fine-tune the model
trainer.train()

# Ensure output directory exists
model_path = "./fine_tuned_model"
if not os.path.exists(model_path):
    os.makedirs(model_path)

# Save the fine-tuned model and tokenizer
model.save_pretrained(model_path)
tokenizer.save_pretrained(model_path)

# Manually save the model's state_dict
torch.save(model.state_dict(), os.path.join(model_path, 'pytorch_model.bin'))

print("Fine-tuning completed. Model saved at", model_path)

# Verify saved files
expected_files = [
    'config.json',
    'pytorch_model.bin',
    'special_tokens_map.json',
    'tokenizer_config.json',
    'vocab.json',
    'merges.txt'
]

saved_files = os.listdir(model_path)
missing_files = [file for file in expected_files if file not in saved_files]

if missing_files:
    print(f"Missing files: {missing_files}")
else:
    print("All necessary files are present.")
