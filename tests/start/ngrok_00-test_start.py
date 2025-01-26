import subprocess

def start_ngrok():
    # Llama al archivo .BAT
    process = subprocess.Popen(
        ["start_ngrok.bat"],  # Nombre del archivo .BAT
        stdout=subprocess.PIPE,  # Captura la salida estándar
        stderr=subprocess.PIPE,  # Captura los errores
        text=True,               # Decodifica la salida como texto
        shell=True               # Necesario para ejecutar .BAT en Windows
    )

    print(f"Ngrok start sundomain free ejecutado con PID: {process.pid}.")

if __name__ == "__main__":
    start_ngrok()