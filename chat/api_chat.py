# chat/deepseek_api.py
import requests
import json
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

def get_response(prompt, model="deepseek-chat"):
    try:
        if not hasattr(settings, 'sk-68f1b2a3a1434bd098c9170f4b5ec73d'):
            raise ImproperlyConfigured("DeepSeek API key no configurada")
        
        api_key = settings.DEEPSEEK_API_KEY
        endpoint = "https://api.deepseek.com/v1/chat/completions"  # Verificar en documentación real
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }

        payload = {
            "model": model,
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.7,
            "max_tokens": 1000
        }

        response = requests.post(
            endpoint,
            headers=headers,
            data=json.dumps(payload),
            timeout=30  # Segundos
        )

        if response.status_code == 200:
            response_data = response.json()
            return response_data['choices'][0]['message']['content'].strip()
        else:
            return f"Error en la API: {response.status_code} - {response.text}"

    except requests.exceptions.RequestException as e:
        return f"Error de conexión: {str(e)}"
    except Exception as e:
        return f"Error inesperado: {str(e)}"