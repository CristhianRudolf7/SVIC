import re

def extraer_codigo_python(texto):
    patron = r"```python\n(.*?)```"
    match = re.search(patron, texto, re.DOTALL)
    if match:
        return match.group(1).strip()
    else:
        return None

# Ejemplo de uso:
texto_ejemplo = """
Aquí hay algo de texto antes del código.
```python
def saludar(nombre):
    print(f"Hola, {nombre}!")

saludar("Mundo")
# Otro bloque de código
x = 10
y = 20
print(x + y)```
"""
codigo_extraido = extraer_codigo_python(texto_ejemplo)

if codigo_extraido:
    print("Código Python extraído:")
    print(codigo_extraido)
else:
    print("No se encontró código Python en el formato esperado.")