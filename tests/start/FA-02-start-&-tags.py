# Description: FastAPI example with a simple root path
# Author: @DanielChristello - 2024
# Tercer código de FastAPI
# tags=["Home"] is used to group the paths on the explorer

from fastapi import FastAPI

app = FastAPI()

app.title = "Primer API con FastAPI"
app.version = "0.2"

@app.get("/", tags=["Home"])   # Tag and Decorator for the root path
def read_root():
    return {"Hola": "Mundo"}

@app.get("/home", tags=["Home"])   # Tag and Decorator for the root path
def read_root():
    return {"Hola": "Mundo"}

# Para ejecutar directamente el archivo
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000) 
    
# tags=["Home"] is used to group the paths on the explorer
# Test http://localhost:5000/docs#/ to see de GET response of the server on explorer
# Test http://localhost:5000/docs#/Home to see de response of the server on explorer