from django.test import TestCase

# Create your tests here.
import csv
from transformers import GPT2LMHeadModel, GPT2Tokenizer

# Load pre-trained model and tokenizer
tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
model = GPT2LMHeadModel.from_pretrained("gpt2")

# Load successful project data from CSV file
successful_events = []
with open('events.csv', newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        successful_events.append(row)

# Generate event summaries using the language model
for event in successful_events:
    input_text = f"Successful event '{event['title']}'\n\nStart Date: {event['start_date']}\nEnd Date: {event['end_date']}\nDescription: {event['description']}\nTarget Amount: {event['target_amount']}"
    input_ids = tokenizer.encode(input_text, return_tensors="pt")
    output = model.generate(input_ids, max_length=100, num_return_sequences=1)
    summary = tokenizer.decode(output[0], skip_special_tokens=True)
    print(summary)
