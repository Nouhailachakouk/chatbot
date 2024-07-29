from flask import Flask, request, jsonify
from flask_cors import CORS
from transformers import GPT2LMHeadModel, GPT2Tokenizer

app = Flask(__name__)
CORS(app)

# Load the models and tokenizers for both languages
model_path_en = r'C:\Users\User\Documents\CHATBOT\vscode\chatbot.py\final_model2'
model_path_fr = r'C:\Users\User\Documents\CHATBOT\vscode\chatbot.py\final_model'

model_en = GPT2LMHeadModel.from_pretrained(model_path_en)
tokenizer_en = GPT2Tokenizer.from_pretrained(model_path_en)

model_fr = GPT2LMHeadModel.from_pretrained(model_path_fr)
tokenizer_fr = GPT2Tokenizer.from_pretrained(model_path_fr)

@app.route('/generate', methods=['POST'])
def generate_response():
    if request.is_json:
        data = request.get_json()
        prompt = data.get('prompt', '')
        language = data.get('language', 'en')  # Default to English if not specified
        
        # Select the appropriate model and tokenizer
        if language == 'fr':
            model = model_fr
            tokenizer = tokenizer_fr
        else:
            model = model_en
            tokenizer = tokenizer_en
        
        # Log received prompt
        print(f"Received prompt: {prompt} in language: {language}")
        
        # Generate response
        inputs = tokenizer(f"Question: {prompt} Answer:", return_tensors="pt")
        
        # Generate with attention mask
        outputs = model.generate(
            inputs.input_ids,
            attention_mask=inputs.attention_mask,
            max_length=50,
            num_return_sequences=1,
            pad_token_id=tokenizer.eos_token_id
        )
        
        response_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
        
        # Clean the response
        response_text = response_text.replace(f"Question: {prompt} Answer:", "").strip()
        if 'Answer: ' in response_text:
            response_text = response_text.split('Answer: ')[-1]
        
        # Log and return only the response text
        print(f"Generated response: {response_text}")
        return jsonify({'response': response_text.strip()})
    else:
        return jsonify({'error': 'Request must be JSON'}), 400

if __name__ == '__main__':
    app.run(port=5000, debug=False)
