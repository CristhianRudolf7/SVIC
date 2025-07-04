# AIzaSyAAQpaF0tuDW5J7l5HXBJkJCwYoPMvaACM
import google.generativeai as genai

# Configura tu clave API
genai.configure(api_key="AIzaSyAAQpaF0tuDW5J7l5HXBJkJCwYoPMvaACM")

# Ahora puedes crear una instancia del modelo
model = genai.GenerativeModel('gemini-2.5-flash')

# Y luego generar contenido
response = model.generate_content("dame una guia en python")
print(response.text)