function login(){
    fetch(" http://127.0.0.1:8000/login", {
        method : 'GET'
    })
    .then(response => response.json())
    .then(data =>{
        alert(data.mensagem)
    })
}