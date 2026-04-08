import os
import google.generativeai as genai
import json
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

models_to_try = [
    'gemini-1.5-flash',
    'gemini-1.5-pro',
    'gemini-pro'
]

for m_name in models_to_try:
    print(f"\n--- Testing Model: {m_name} ---")
    try:
        model = genai.GenerativeModel(m_name)
        response = model.generate_content(
            "Respond only with the word 'HELLO' in a JSON object: {\"msg\": \"HELLO\"}",
            generation_config=genai.GenerationConfig(
                response_mime_type="application/json"
            )
        )
        print(f"Success with {m_name}: {response.text}")
    except Exception as e:
        print(f"Failed with {m_name}: {e}")
