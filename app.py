from flask import Flask, render_template, request, jsonify
from openai import OpenAI
import pdfplumber
import os

app = Flask(__name__)

# Folosește cheia API din variabilă de mediu
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload():
    file = request.files["file"]
    if not file or not file.filename.endswith(".pdf"):
        return jsonify({"error": "Te rog încarcă un fișier PDF valid."}), 400

    # Citește textul din PDF
    with pdfplumber.open(file) as pdf:
        text = "\n".join(page.extract_text() or "" for page in pdf.pages)

    # Prompt pentru GPT
    prompt = f"""
    Din următorul text al facturii, extrage următoarele informații și returnează în format JSON:
    - Denumire Furnizor
    - Denumire Material
    - Cantitate
    - Pret unitar
    - Pret total

    Text factură:
    {text}
    """

    response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": prompt}],
    temperature=0,
    max_tokens=500,
    response_format={ "type": "json_object" }   # 👈 forțează răspuns JSON valid
)

    answer = response.choices[0].message.content
    return jsonify({"result": answer})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000, debug=True)