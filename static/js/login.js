/*
=========================================================
ProjectStarter

login.js

Gestion de la page de connexion

=========================================================
*/


/*=======================================================
    ELEMENTS
=======================================================*/

const form = document.getElementById("login-form");

const password = document.getElementById("password");

const togglePassword = document.getElementById("toggle-password");

const inputs = document.querySelectorAll("input");


/*=======================================================
    AFFICHER / MASQUER LE MOT DE PASSE
=======================================================*/

togglePassword.addEventListener("click", () => {

    if(password.type === "password"){

        password.type = "text";

        togglePassword.textContent = "🙈";

    }

    else{

        password.type = "password";

        togglePassword.textContent = "👁️";

    }

});


/*=======================================================
    ANIMATION DES CHAMPS
=======================================================*/

inputs.forEach(input => {

    input.addEventListener("focus", () => {

        input.parentElement.classList.add("active");

    });

    input.addEventListener("blur", () => {

        input.parentElement.classList.remove("active");

    });

});


/*=======================================================
    VALIDATION
=======================================================*/

form.addEventListener("submit", (event) => {

    const email = document.getElementById("email").value.trim();

    if(email === ""){

        event.preventDefault();

        alert("Veuillez entrer votre adresse e-mail.");

        return;

    }

    if(password.value.length < 8){

        event.preventDefault();

        alert("Le mot de passe doit contenir au moins 8 caractères.");

        return;

    }

});


/*=======================================================
    CONSOLE
=======================================================*/

console.log("ProjectStarter - Login chargé.");