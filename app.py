from flask import Flask, render_template, request, jsonify
from openai import OpenAI
import os

app = Flask(__name__)

# Inițializează clientul OpenAI cu cheia din variabila de mediu
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

system_message = {
    "role": "system",
    "content": "Ești un asistent prietenos care ajută utilizatorul să învețe limba maghiară. Explică simplu, oferă exemple, corectează greșelile și propune exerciții scurte."
}

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message")

    messages = [
        system_message,
        {"role": "user", "content": user_message}
    ]

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        max_tokens=400,
        temperature=0.7,
    )

    answer = response.choices[0].message.content
    return jsonify({"answer": answer})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)