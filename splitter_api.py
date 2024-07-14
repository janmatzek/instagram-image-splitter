from fastapi import FastAPI


app = FastAPI()

@app.get("/")
def read_root():
    return {"/health": "GET - Health Check"}

@app.get("/health")
def health_check():
    return {"Status": "Healthy"}