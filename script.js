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