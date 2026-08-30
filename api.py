from fastapi import FastAPI

app = FastAPI()

@app.get("/login")
def LoginUser():
    return {"hello" : "World"}