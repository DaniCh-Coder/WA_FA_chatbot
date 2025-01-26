# Description: FastAPI example with a simple root path
# Author: @DanielChristello - 2024
# Segundo códgio de FastAPI

from fastapi import FastAPI

app = FastAPI()

app.title = "Primer API con FastAPI"
app.version = "0.1"

@app.get("/")   # Decorator for the root path
def read_root():
    return {"Hola": "Mundo"}

# Para ejecutar directamente el archivo
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000) 
    
# Test app.title and app.version with: http://localhost:5000/docs
# Expected output: Swagger UI with the API documentation
# Test FastAPI with: http://localhost:5000/redoc
# Expected output: ReDoc UI with the API documentation