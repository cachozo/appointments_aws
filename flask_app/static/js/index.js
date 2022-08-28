var formLogin = document.getElementById('formLogin'); //Obteniendo el formulario

/* Vamos a escuchar cuando se realice el evento ON SUBMIT */
formLogin.onsubmit = function (event) {
    event.preventDefault(); /* Previene el comportamiento por default de mi formulario */

    //Creamos una variable con todos los datos del formulario
    var formulario = new FormData(formLogin);
    /*
    formulario = {
        "email": "elena@codingdojo.com",
        "password": "1234"
     } 
     */

    fetch("/login", {method: 'POST', body: formulario})
        .then(response => response.json())
        .then(data => {
            console.log(data);

            if(data.message == "correcto") {
                window.location.href = "/dashboard";
            }

            var mensajeAlerta = document.getElementById('mensajeAlerta'); //El elemento con identificador mensajeAlerta
            mensajeAlerta.innerText = data.message;
            mensajeAlerta.classList.add('alert');
            mensajeAlerta.classList.add('alert-danger');
            
        });
        
}