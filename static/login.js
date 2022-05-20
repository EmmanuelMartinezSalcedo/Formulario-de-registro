const submitButton=document.getElementById("boton");

const input3 = document.getElementById("correo");
const input4 = document.getElementById("contraseña");

input3.addEventListener('keyup', (e) => {
    const value = e.currentTarget.value;
    submitButton.disabled=false;
    if (value == ""){
        submitButton.disabled = true;
    }
});
input4.addEventListener('keyup', (e) => {
    const value = e.currentTarget.value;
    submitButton.disabled=false;
    if (value == ""){
        submitButton.disabled = true;
    }
});
