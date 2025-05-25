import os

# Ingresar texto a buscar
texto_buscar = input("Ingresa el texto a buscar: ")

# Recorrer todos los archivos .py en el directorio actual y subdirectorios
for root, dirs, files in os.walk("."):
    for file in files:
        if file.endswith(".py") or file.endswith(".html"):
            ruta_archivo = os.path.join(root, file)
            try:
                with open(ruta_archivo, "r", encoding="utf-8") as f:
                    contenido = f.read()
                    if texto_buscar in contenido:
                        print(f"Encontrado en: {ruta_archivo}")
            except Exception as e:
                print(f"No se pudo leer {ruta_archivo}: {e}")
