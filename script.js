function login(){
    fetch(" http://127.0.0.1:8000/login", {
        method : 'GET'
    })
    .then(data => Response.json)
    alert(data)
}