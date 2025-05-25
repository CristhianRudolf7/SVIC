from openai import OpenAI

client = OpenAI(
    api_key="sk-68f1b2a3a1434bd098c9170f4b5ec73d", base_url="https://api.deepseek.com"
)

response = client.chat.completions.create(
    model="deepseek-chat",
    messages=[
        {"role": "system", "content": "You are a helpful assistant"},
        {"role": "user", "content": "Cual es la derivada de seno de x"},
    ],
    stream=False,
)

print(response.choices[0].message.content)
