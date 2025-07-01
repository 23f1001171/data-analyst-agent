import os
import httpx
from typing import Dict, Any

class LLMService:
    def __init__(self):
        self.api_base = os.getenv("OPENAI_API_BASE", "https://aiproxy.sanand.workers.dev/openai/")
        self.api_key = os.getenv("OPENAI_API_KEY")
    
    async def analyze(self, prompt: str, context: str = None) -> str:
        messages = [
            {
                "role": "system",
                "content": "You are a data analysis assistant. Help with data sourcing, preparation, analysis, and visualization."
            },
            {"role": "user", "content": prompt}
        ]
        
        if context:
            messages.insert(1, {"role": "system", "content": context})
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    f"{self.api_base}chat/completions",
                    json={
                        "model": "gpt-4",
                        "messages": messages,
                        "temperature": 0.1
                    },
                    timeout=60.0
                )
                response.raise_for_status()
                return response.json()["choices"][0]["message"]["content"]
            except httpx.HTTPStatusError as e:
                raise Exception(f"LLM API error: {e.response.text}")
            except Exception as e:
                raise Exception(f"LLM communication error: {str(e)}")