window.onload = function(){
    getReqList();
}
function getReqList(){
    fetch("http://127.0.0.1:8000/showsRequests", {
        method : 'GET'
    })
    .then(async response =>{
        if (response.status === 429){
            const data = await response.json().catch(() => ({}));
            localStorage.setItem("waitTime", data.wait_time)
            console.log(data.wait_time)
            window.location.href = "429.html"
            return;
        }
        if (!response.ok){
            alert("Erro no CORS")
        }
        const data = await response.json()
        const reqTableactions = document.getElementById("Req-table")
        console.log(data)
        const reqListActions = data.req_list
        reqListActions.forEach(req =>{
            const tr = document.createElement("tr")
            tr.innerHTML = `
                <td>${req.origem}</td>
                <td>${req.quantidade}</td>
            `
            reqTableactions.appendChild(tr)
        })

        const callByIp = data.IP_req
        const reqTableIp = document.getElementById("Req-table-IP")
        callByIp.forEach(ip =>{
            const tr = document.createElement("tr")
            tr.innerHTML = `
                <td>${ip.IP}</td>
                <td>${ip.quantidade}</td>
            
            `
            reqTableIp.appendChild(tr)
        })


    })
}





function login() {
    fetch("http://127.0.0.1:8000/login", {
        method: "GET"
    })
    .then(async response => {
        if (response.status === 429) {
            const data = await response.json().catch(() => ({}));
            localStorage.setItem("waitTime", data.wait_time)
            console.log(data.wait_time)
            window.location.href = "429.html"
            return;
        }

        if (!response.ok) {
            throw new Error("erro servidor");
        }

        const data = await response.json();
    })
    .catch(error => {
        console.error(error);
        alert("Erro de conexão ou CORS");
    });
}

function secondRoute(){
    fetch("http://127.0.0.1:8000/increaseCount", {
        method : 'GET'
    })
    .then(async response =>{
        if (response.status === 429){
            const data = await response.json().catch(() => ({}));
            window.location.href = "429.html"
            return;
        }
        if (!response.ok) {
            throw new Error("erro servidor");
        }
        const data = await response.json();
        const contagem = document.getElementById("contagem")
        contagem.textContent = data.num
    })
}
function thirdRoute(){
    fetch("http://127.0.0.1:8000/increaseCount2", {
        method : 'GET'
    })
    .then(async response =>{
        if (response.status === 429){
            const data = await response.json().catch(() => ({}));
            window.location.href = "429.html"
            return;
        }
        if (!response.ok) {
            throw new Error("erro servidor");
        }
        const data = await response.json();
        const contagem = document.getElementById("contagem2")
        contagem.textContent = data.num
    })
}