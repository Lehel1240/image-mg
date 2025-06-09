from flask import Flask, render_template, request, jsonify
from together import Together

app = Flask(__name__)  # <-- Ez legyen az első

API_KEY = "39f9487dcddb59a5eb5aef41cb9da258d630db44533f12369ae0334c2f49769a"

if not API_KEY:
    raise ValueError("Az API kulcs nincs beállítva!")

client = Together(api_key=API_KEY)

BOT_NAME = "Alvid"
CREATOR_NAME = "Lehel"

# Közös beszélgetési előzmény (élesben session-ben tárold!)
conversation_history = [
    {
        "role": "system",
        "content": f"You are {BOT_NAME}, a helpful and intelligent chatbot created by {CREATOR_NAME}. Your answers should be insightful and well-formatted in Markdown."
    }
]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about_page():
    return render_template('about.html')

@app.route('/docs')
def docs_page():
    return render_template('docs.html')

@app.route('/chat')
def chat_page():
    return render_template('chat.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    global conversation_history
    user_input = request.json.get('message', '')

    if not user_input:
        return jsonify({'error': 'Empty message received'}), 400

    conversation_history.append({"role": "user", "content": user_input})

    try:
        response = client.chat.completions.create(
            model="meta-llama/Llama-3.3-70B-Instruct-Turbo-Free",
            messages=conversation_history,
            max_tokens=2048,
            stream=False
        )
        reply = response.choices[0].message.content.strip()

        conversation_history.append({"role": "assistant", "content": reply})

        return jsonify({'reply': reply})

    except Exception as e:
        print(f"API Error: {e}")
        error_message = 'Elnézést, egy belső hiba történt. Kérlek, próbáld meg később újra.'
        conversation_history.pop()
        return jsonify({'reply': error_message}), 500


import os

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)


