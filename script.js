function login(){
    fetch(" http://127.0.0.1:8000/login", {
        method : 'GET'
    })
    .then( async response => {
        if (response.status === 429){
            alert("rate limit API")
            return response.json()
        }
        if (response.ok){
            return response.json()
        }
        if (!response){
            throw new Error("erro servidor");
        }
        const data = await response.json()
        console.log(data.mensagem)
    })
    
    
}