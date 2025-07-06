import google.generativeai as genai
genai.configure(api_key="AIzaSyAAQpaF0tuDW5J7l5HXBJkJCwYoPMvaACM")
model = genai.GenerativeModel('gemini-2.5-flash')
response = model.generate_content("dame una guia en python")
print(response.text)