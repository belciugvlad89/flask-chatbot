from flask import Flask, render_template, request, jsonify
from openai import OpenAI
import os

app = Flask(__name__)

# Inițializează clientul OpenAI cu cheia din variabila de mediu
client = OpenAI(api_key="skproj-0fVlFGaBkPrbIZ_D6Ek3YBGDYO7r2nRF8yDTvb6MOFmRczPqa4fYZRY83GOcmFw1vXMIBgw8qeT3BlbkFJfxZe_h50WK2j8g869LBG4aL81ytn3q7Lw5MUyYH69mC63SgmyoTwGfgPWRPyJN-CGXk6Es4g0A")

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
    app.run(debug=True)
