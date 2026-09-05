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

calls_by_IP =[]








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
    chave = (client_ip, request.url.path)

    if chave not in ips_historic:
        ips_historic[chave] = []

    limit_time = now - timedelta(seconds=time_skip)
    ips_historic[chave] = [
        t for t in ips_historic[chave]
        if t > limit_time
    ]
    

    if len(ips_historic[chave]) >= req_limit:
        oldest_request = ips_historic[chave][0]
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
    ips_historic[chave].append(now)
    response = await call_next(request)
    return response

login_req_count = 0
@app.get("/login", openapi_extra={"req_limit" : 5, "time_skip" : 60})
def LoginUser(request : Request):
    global calls_by_IP
    if calls_by_IP is None:
        calls_by_IP=[]
    ip_atual = request.client.host
    encontrado = False

    for item in calls_by_IP:
        if item['IP'] == ip_atual:
            item['quantidade'] +=1
            encontrado = True
            break

    if not encontrado:
        calls_by_IP.append({
            'IP': ip_atual,
            'quantidade' : 1
        })




    global login_req_count 
    login_req_count +=1
    return {"mensagem" : "teste"}


num = 0
num_req_count = 0
@app.get("/increaseCount", openapi_extra={"req_limit" : 5, "time_skip": 120})
def increaseCount(request: Request):
    global calls_by_IP
    if calls_by_IP is None:
            calls_by_IP=[]
    ip_atual = request.client.host
    encontrado = False
    
    for item in calls_by_IP:
        if item['IP'] == ip_atual:
            item['quantidade'] +=1
            encontrado = True
            break
    
    if not encontrado:
        calls_by_IP.append({
            'IP': ip_atual,
            'quantidade' : 1
        })
        
    global num
    global num_req_count
    num_req_count +=1
    num += 1
    return {"num" : num}


num2 = 0
num2_req_count = 0
@app.get("/increaseCount2", openapi_extra={"req_limit": 60, "time_skip": 120})
def increaseCount2(request: Request):
    global calls_by_IP
    if calls_by_IP is None:
        calls_by_IP = []
    encontrado = False
    for item in calls_by_IP:
        if item['IP'] == request.client.host:
            item['quantidade'] += 1
            encontrado = True
            break

    if not encontrado:
        calls_by_IP.append({
            'IP': request.client.host,
            'quantidade' : 1
        })
    global num2
    global num2_req_count
    num2_req_count +=1
    num2+=1
    return {"num": num2}
        


@app.get("/showsRequests", openapi_extra={"req_limit": 5, "time_skip": 30})
def mostrarRequests():
    req_List = [
        {
            "origem" : "Requisições Login",
            "quantidade" : login_req_count
        },
        {
            "origem" : "Requisições Contagem",
            "quantidade" : num_req_count
        },
        {
            "origem" : "Requisições Contagem 2",
            'quantidade' : num2_req_count
         }
    ]
    return {"req_list" : req_List, "IP_req" : calls_by_IP}