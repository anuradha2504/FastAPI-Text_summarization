from fastapi import FastAPI
from pydantic import BaseModel
import requests
import os

# ✅ Create FastAPI app instance
app = FastAPI()

# Load your Gemini API key , Define API endpoint URL
GEMINI_API_KEY = "AIzaSyCC-IUMgLphIyIoNFUwu7k0x1A793NjI-Q"
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"

# Define input model (text + summary length).
class SummarizationRequest(BaseModel):
    prompt: str
    max_tokens: int = 500  # default summary length

# Define API endpoint /summarize ,Accepts SummarizationRequest body and implement logic to call Gemini API

@app.post("/summarize")
def summarize_text(request: SummarizationRequest):
    headers = {
        "Content-Type": "application/json"
    }
    params = {
        "key": GEMINI_API_KEY
    }

#Format request as per Gemini API specs.
    payload = {
        "contents": [
            {"parts": [{"text": f"Summarize the following text in a concise and clear way:\n\n{request.prompt}"}]}
        ],
        "generationConfig": {
            "maxOutputTokens": request.max_tokens
        }
    }

#Make POST request to Gemini API and If error → return error JSON.
    response = requests.post(GEMINI_API_URL, headers=headers, params=params, json=payload)

    if response.status_code != 200:
        return {"error": response.text}
    
    #Parse API response safely.

    result = response.json()

    # Extract summary text.
    data = response.json()
    summary_text = data.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "")

    # Return as JSON response

    return {"summary": summary_text}
