import google.generativeai as genai
from backend.sysPrompt import system_prompt

genai.configure(api_key="AIzaSyDRD1eS5F8mOkkLq7iAkJNzuMmqPOXbnWk")
model = genai.GenerativeModel("gemini-2.5-pro")

def gemini_client(client_data: str) -> str:
    try:
        prompt = f"""{system_prompt(client_data)}
        
        Provide recommendations in this JSON format:
        {{
            "recommendations": [
                {{
                    "product_id": "string",
                    "product_name": "string",
                    "reason": "string",
                    "risk_level": "string",
                    "confidence": float
                }}
            ]
        }}
        """
        
        chat = model.start_chat(history=[])
        response = chat.send_message(prompt)
        return response.text.strip()
    except Exception as e:
        print(f"Gemini API error: {str(e)}")
        return '{"recommendations": []}'