from fastapi import FastAPI, Request, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime, timedelta
app = FastAPI()
origins = [
    "http://127.0.0.1:5500",    
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,           
    allow_credentials=True,
    allow_methods=["*"],              
    allow_headers=["*"],             
)
ips_historic ={}
req_limit = 10
time_skip = 60
@app.middleware("http")
async def rate_limit_ip(request : Request, call_next):
    client_ip = request.client.host
    now = datetime.now()

    if client_ip not in ips_historic:
        ips_historic[client_ip] = []

    limit_time = now - timedelta(seconds=time_skip)
    ips_historic[client_ip] = [t for t in ips_historic[client_ip] if t > limit_time]

    if len(ips_historic[client_ip]) >= req_limit:
        return JSONResponse(
    status_code=429,
    content={
        "sucesso": False,
        "mensagem": "Rate Limit excedido"
        },
        headers={
            "Access-Control-Allow-Origin": "http://127.0.0.1:5500",
            "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
            "Access-Control-Allow-Headers": "*"
        }
)
    ips_historic[client_ip].append(now)
    
    response = await call_next(request)
    return response

@app.get("/login")
def LoginUser():
    return {"mensagem" : "teste"}