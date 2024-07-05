from flask import Flask, request, jsonify
from transformers import GPT2LMHeadModel, GPT2Tokenizer
import torch

app = Flask(__name__)

# Load the fine-tuned model and tokenizer
model_path = "C:\\Users\\shara\\CHATBOT\\fine_tuned_model"
tokenizer = GPT2Tokenizer.from_pretrained(model_path)
model = GPT2LMHeadModel.from_pretrained(model_path)

@app.route('/')
def home():
    return "Welcome to the Chatbot API!"

@app.route('/generate', methods=['POST'])
def generate():
    data = request.json
    if 'input_text' not in data:
        return jsonify({"error": "No input_text field provided in JSON"}), 400

    input_text = data['input_text']
    inputs = tokenizer(input_text, return_tensors="pt")

    # Generate a response
    with torch.no_grad():
        outputs = model.generate(
            inputs.input_ids,
            max_length=150,
            num_return_sequences=1,
            no_repeat_ngram_size=2,
            top_p=0.95,
            top_k=60
        )

    generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return jsonify({"generated_text": generated_text})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
