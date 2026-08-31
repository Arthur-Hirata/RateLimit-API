function login() {
    fetch("http://127.0.0.1:8000/login", {
        method: "GET"
    })
    .then(async response => {
        if (response.status === 429) {
            const data = await response.json().catch(() => ({}));
            alert(data.detail || "Rate limit excedido");
            return;
        }

        if (!response.ok) {
            throw new Error("erro servidor");
        }

        const data = await response.json();
        console.log(data);
    })
    .catch(error => {
        console.error(error);
        alert("Erro de conexão ou CORS");
    });
}