from fastapi import FastAPI
from pydantic import BaseModel
import requests
import os

# ✅ Create FastAPI app instance
app = FastAPI()

# Load your Gemini API key , Define API endpoint URL
GEMINI_API_KEY = "
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"

# Define input model (text + summary length).
class SummarizationRequest(BaseModel):
    text: str
    max_tokens: int = 15  # default summary length

# Define API endpoint /summarize ,Accepts SummarizationRequest body and implement logic to call Gemini API

@app.post("/summarize")
def summarize_text(request: SummarizationRequest):
    headers = {
        "Content-Type": "application/json"
    }
    params = {
        "key": GEMINI_API_KEY
    }

#Added API key to headers.Build summarization prompt.
   
    prompt = (
    f"Summarize the following passage in about {request.max_tokens} words. "
    f"Provide a concise summary without copying text:\n\n{request.text}"
    )
#Format request as per Gemini API specs.
    payload = {
        "contents": [
            {"parts": [{"text": prompt}]}
        ]
    }

#Make POST request to Gemini API and If error → return error JSON.
    response = requests.post(GEMINI_API_URL, headers=headers, params=params, json=payload)

    if response.status_code != 200:
        return {"error": response.text}
    
    #Parse API response safely.

    result = response.json()

    # Extract summary text.
    try:
        summary = result["candidates"][0]["content"]["parts"][0]["text"].strip()
    except (KeyError, IndexError):
        return {"error": "Unexpected response format", "response": result}

    # Return as JSON response

    return {"summary": summary}