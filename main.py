import pandas as pd
import re
import os
import torch
from sklearn.model_selection import train_test_split
from datasets import load_dataset
from transformers import (
    AutoTokenizer,
    AutoModelForCausalLM,
    TrainingArguments,
    Trainer,
    DataCollatorForLanguageModeling,
)
import time
import psutil
import gc

# --- 1. Data Preparation ---

# Load the dataset
try:
    df = pd.read_csv('ai-medical-chatbot.csv')
except FileNotFoundError:
    print("Error: 'ai-medical-chatbot.csv' not found.")
    print("Please make sure the dataset file is in the same directory as your script.")
    exit()

# Create the instruction-formatted text column
df['text'] = '<s>[INST] ' + df['Patient'].astype(str) + ' [/INST] ' + df['Doctor'].astype(str) + '</s>'

# Define a function to clean the text
def clean_text(text):
    if not isinstance(text, str):
        return ""
    text = re.sub(r'http\S+', '', text)      # Remove URLs
    text = re.sub(r'<.*?>', '', text)       # Remove HTML tags
    text = text.lower()                     # Convert to lowercase
    text = re.sub(r'[^a-zA-Z0-9\s.,!?]', '', text) # Remove special characters
    text = re.sub(r'\s+', ' ', text).strip() # Remove extra whitespace
    return text

# Apply the cleaning function
df['text'] = df['text'].apply(clean_text)

# For CPU training, we'll use a smaller subset to make training faster
# You can adjust this based on your needs and CPU capabilities
df = df.sample(min(1000, len(df)), random_state=42)

# Split data into training and validation sets
train_df, val_df = train_test_split(df, test_size=0.1, random_state=42)

# Save to temporary CSV files for loading with the 'datasets' library
train_df.to_csv('train_dataset.csv', index=False)
val_df.to_csv('val_dataset.csv', index=False)
print("Data preparation and cleaning complete.")

# --- 2. Tokenization ---

# Define the pre-trained model you want to fine-tune
# Using a smaller model for CPU training
model_name = "microsoft/DialoGPT-medium"  # Smaller model better suited for CPU

# Initialize the tokenizer
tokenizer = AutoTokenizer.from_pretrained(model_name)
if tokenizer.pad_token is None:
    tokenizer.pad_token = tokenizer.eos_token

# Load the datasets from the CSV files
train_dataset = load_dataset('csv', data_files='train_dataset.csv', split='train')
val_dataset = load_dataset('csv', data_files='val_dataset.csv', split='train')

# Define a function to tokenize the text
def tokenize_function(examples):
    return tokenizer(
        examples['text'], 
        truncation=True, 
        padding='max_length', 
        max_length=256  # Reduced max_length for faster processing
    )

# Apply tokenization to the datasets
tokenized_train_dataset = train_dataset.map(tokenize_function, batched=True)
tokenized_val_dataset = val_dataset.map(tokenize_function, batched=True)

# Remove text column as it's no longer needed
tokenized_train_dataset = tokenized_train_dataset.remove_columns(['text'])
tokenized_val_dataset = tokenized_val_dataset.remove_columns(['text'])

# Set format for PyTorch
tokenized_train_dataset.set_format("torch")
tokenized_val_dataset.set_format("torch")

print("Tokenization complete.")

# --- 3. Model Loading and Training ---

# Load the pre-trained model for CPU
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    torch_dtype=torch.float32,  # Use float32 for CPU
)

# Move model to CPU explicitly
device = torch.device("cpu")
model.to(device)

# Enable gradient checkpointing to save memory
model.gradient_checkpointing_enable()

# Define training arguments optimized for CPU
training_args = TrainingArguments(
    output_dir="./results",
    num_train_epochs=2,                 # Reduced epochs for faster training
    per_device_train_batch_size=1,      # Small batch size for CPU
    per_device_eval_batch_size=1,       # Small batch size for evaluation
    gradient_accumulation_steps=8,      # Accumulate gradients to simulate larger batch
    warmup_steps=100,                   # Reduced warmup steps
    weight_decay=0.01,
    logging_dir="./logs",
    logging_steps=5,                    # Log more frequently to track progress
    eval_strategy="epoch",
    save_strategy="epoch",
    load_best_model_at_end=True,
    dataloader_num_workers=4,           # Use multiple CPU cores for data loading
    fp16=False,                         # Disable mixed precision (not well supported on CPU)
    optim="adamw_torch",                # Use standard AdamW optimizer
    learning_rate=5e-5,                  # Slightly higher learning rate
    report_to="none",                    # Disable reporting to save resources
)

# Initialize the Trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_train_dataset,
    eval_dataset=tokenized_val_dataset,
    data_collator=DataCollatorForLanguageModeling(tokenizer=tokenizer, mlm=False),
)

# --- 4. Start Fine-Tuning ---
try:
    print("Starting fine-tuning on CPU...")
    print(f"CPU cores available: {os.cpu_count()}")
    print(f"Memory available: {psutil.virtual_memory().available / (1024 ** 3):.2f} GB")
    
    start_time = time.time()
    
    trainer.train()
    
    end_time = time.time()
    print(f"Fine-tuning complete in {end_time - start_time:.2f} seconds.")

    # Save the fine-tuned model and tokenizer
    final_model_path = './fine-tuned-medical-chatbot-cpu'
    model.save_pretrained(final_model_path)
    tokenizer.save_pretrained(final_model_path)
    print(f"Model saved successfully to '{final_model_path}'")

except Exception as e:
    print("\n========================= ERROR ==========================")
    print(f"An error occurred during training: {e}")
    print("\nCommon issues to check:")
    print("1. Memory: You might be out of memory. Try reducing the dataset size further.")
    print("2. Model size: Consider using an even smaller model.")
    print("3. Dependencies: Ensure all required libraries are correctly installed.")
    print("==========================================================")

# Clean up memory
gc.collect()