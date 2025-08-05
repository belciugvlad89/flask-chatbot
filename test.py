from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "Test bot"},
        {"role": "user", "content": "Salut, funcționează?"}
    ],
    max_tokens=50
)

print(response.choices[0].message.content)