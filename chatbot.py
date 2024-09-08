import httpx
import openai
from config import settings

# Load OpenAI API key
openai.api_key = settings.openai_api_key
hugging_key = settings.hugging_face_api_key


async def create_huggingface_response(prompt: str) -> str:
    """Generate a response using Hugging Face's Inference API (async with httpx)."""
    api_url = "https://api-inference.huggingface.co/models/gpt2"  # You can change models here
    headers = {"Authorization": f"Bearer {hugging_key}"}
    payload = {"inputs": prompt}

    async with httpx.AsyncClient() as client:
        response = await client.post(api_url, headers=headers, json=payload)

    if response.status_code != 200:
        raise Exception(f"API request failed: {response.status_code}, {response.text}")
    print(response.json())
    return response.json()[0]["generated_text"].strip()
