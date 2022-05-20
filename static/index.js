const submitButton=document.getElementById("boton");
const input1 = document.getElementById("nombre");
const input2 = document.getElementById("apellido");
const input3 = document.getElementById("correo");
const input4 = document.getElementById("contraseña");

const input5 = document.getElementById("fecha");

const input6 = document.getElementById("sexo");

input1.addEventListener('keyup', (e) => {
    const value = e.currentTarget.value;
    submitButton.disabled=false;
    if (value == ""){
        submitButton.disabled = true;
    }
});
input2.addEventListener('keyup', (e) => {
    const value = e.currentTarget.value;
    submitButton.disabled=false;
    if (value == ""){
        submitButton.disabled = true;
    }
});
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
input5.addEventListener('click', (e) => {
    const value = e.currentTarget.value;
    submitButton.disabled=false;
    if (value == "dd/mm/aaaa"){
        submitButton.disabled = true;
    }
});
input6.addEventListener('change', (e) => {
    const value = e.currentTarget.value;
    submitButton.disabled=false;
    if (value == "--Sexo--"){
        submitButton.disabled = true;
    }
});