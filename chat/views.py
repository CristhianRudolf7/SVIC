from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import google.generativeai as genai

genai.configure(api_key="AIzaSyAAQpaF0tuDW5J7l5HXBJkJCwYoPMvaACM")
model = genai.GenerativeModel('gemini-2.5-flash')

def chatView(request):
    return render(request, 'chat/chat.html')

@csrf_exempt
def chatApi(request):
    if request.method == 'POST':
        payload = json.loads(request.body)
        user_msg = payload.get('message', '')
        resp = model.generate_content(user_msg)
        return JsonResponse({'text': resp.text})
    return JsonResponse({'error': 'Método no soportado'}, status=405)