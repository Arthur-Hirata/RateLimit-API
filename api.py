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
@app.middleware("http")
async def rate_limit_ip(request : Request, call_next):
    client_ip = request.client.host
    route = request.scope.get("route")
    time_skip = 60
    req_limit = 10

    for route in app.routes:
        if hasattr(route, 'path') and route.path == request.url.path:
            extra_dic = getattr(route, "openapi_extra", {})
            req_limit = extra_dic.get("req_limit", 10)
            time_skip = extra_dic.get("time_skip", 60)

    now = datetime.now()

    if client_ip not in ips_historic:
        ips_historic[client_ip] = []

    limit_time = now - timedelta(seconds=time_skip)
    ips_historic[client_ip] = [t for t in ips_historic[client_ip] if t > limit_time]
    

    if len(ips_historic[client_ip]) >= req_limit:
        oldest_request = ips_historic[client_ip][0]
        wait_time = max(
        0,
        int((oldest_request + timedelta(seconds=time_skip) - now).total_seconds())
        )
        return JSONResponse(
    status_code=429,
    content={
        "sucesso": False,
        "mensagem": "Rate Limit excedido",
        "wait_time" : wait_time
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

login_req_count = 0
@app.get("/login", openapi_extra={"req_limit" : 5, "time_skip" : 60})
def LoginUser():
    global login_req_count 
    login_req_count +=1
    return {"mensagem" : "teste"}


num = 0
num_req_count = 0
@app.get("/increaseCount", openapi_extra={"req_limit" : 60, "time_skip": 120})
def increaseCount():
    global num
    global num_req_count
    num_req_count +=1
    num += 1
    return {"num" : num}


@app.get("/showsRequests", openapi_extra={"req_limit": 120, "time_skip": 30})
def mostrarRequests():
    req_List = [
        {
            "origem" : "Requisições Login",
            "quantidade" : login_req_count
        },
        {
            "origem" : "Requisições Contagem",
            "quantidade" : num_req_count
        }
    ]
    return {"req_list" : req_List}