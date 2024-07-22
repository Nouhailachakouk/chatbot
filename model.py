from transformers import GPT2LMHeadModel, GPT2Tokenizer, Trainer, TrainingArguments
import pandas as pd
from datasets import Dataset

# Load data
data_file = r'C:\Users\User\Documents\CHATBOT\vscode\chatbot.py\conversation.csv'
data = pd.read_csv(data_file, header=None, names=['question', 'answer'])
dataset = Dataset.from_pandas(data)

# Preprocess data
def format_examples(example):
    return {"text": f"Question: {example['question']} Answer: {example['answer']}"}
dataset = dataset.map(format_examples).remove_columns(['question', 'answer'])

# Split dataset
split_dataset = dataset.train_test_split(test_size=0.1)
train_dataset = split_dataset['train']
eval_dataset = split_dataset['test']

# Tokenize data
tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
tokenizer.pad_token = tokenizer.eos_token
model = GPT2LMHeadModel.from_pretrained("gpt2")
model.config.pad_token_id = tokenizer.pad_token_id

def tokenize_function(examples):
    encodings = tokenizer(examples['text'], padding='max_length', truncation=True, max_length=128)
    encodings['labels'] = encodings['input_ids']
    return encodings

tokenized_train_dataset = train_dataset.map(tokenize_function, batched=True)
tokenized_eval_dataset = eval_dataset.map(tokenize_function, batched=True)

# Training arguments
training_args = TrainingArguments(
    output_dir='./results',
    num_train_epochs=3,
    per_device_train_batch_size=4,
    save_steps=10_000,
    save_total_limit=2,
    logging_dir='./logs',
    logging_steps=500,
    fp16=True,  # Mixed precision
)

# Initialize Trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_train_dataset,
    eval_dataset=tokenized_eval_dataset,
)

# Train
trainer.train()

# Evaluate
results = trainer.evaluate()
print(results)

# Save model
model.save_pretrained('./final_model')
tokenizer.save_pretrained('./final_model')
