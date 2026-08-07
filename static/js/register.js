/*
=========================================================
ProjectStarter

register.js

Gestion de la page d'inscription

Partie 1

=========================================================
*/


/*=======================================================
    ELEMENTS
=======================================================*/

const form = document.getElementById("register-form");

const password = document.getElementById("password");

const confirmPassword = document.getElementById("confirm_password");

const togglePassword = document.getElementById("toggle-password");

const toggleConfirm = document.getElementById("toggle-confirm");

const strengthBar = document.getElementById("strength-bar");

const passwordMessage = document.getElementById("password-message");



/*=======================================================
    AFFICHER / MASQUER MOT DE PASSE
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



toggleConfirm.addEventListener("click", () => {

    if(confirmPassword.type === "password"){

        confirmPassword.type = "text";

        toggleConfirm.textContent = "🙈";

    }

    else{

        confirmPassword.type = "password";

        toggleConfirm.textContent = "👁️";

    }

});

/*=======================================================
    FORCE DU MOT DE PASSE
=======================================================*/

password.addEventListener("input", () => {

    const value = password.value;

    let score = 0;

    if(value.length >= 8){

        score++;

    }

    if(/[A-Z]/.test(value)){

        score++;

    }

    if(/[a-z]/.test(value)){

        score++;

    }

    if(/[0-9]/.test(value)){

        score++;

    }

    if(/[^A-Za-z0-9]/.test(value)){

        score++;

    }

    switch(score){

        case 0:
        case 1:

            strengthBar.style.width = "20%";
            strengthBar.style.background = "#ef4444";

            passwordMessage.textContent = "Mot de passe très faible.";

            break;

        case 2:

            strengthBar.style.width = "40%";
            strengthBar.style.background = "#f97316";

            passwordMessage.textContent = "Mot de passe faible.";

            break;

        case 3:

            strengthBar.style.width = "60%";
            strengthBar.style.background = "#eab308";

            passwordMessage.textContent = "Mot de passe moyen.";

            break;

        case 4:

            strengthBar.style.width = "80%";
            strengthBar.style.background = "#22c55e";

            passwordMessage.textContent = "Bon mot de passe.";

            break;

        case 5:

            strengthBar.style.width = "100%";
            strengthBar.style.background = "#16a34a";

            passwordMessage.textContent = "Excellent mot de passe.";

            break;

    }

});



/*=======================================================
    VERIFICATION DES MOTS DE PASSE
=======================================================*/

confirmPassword.addEventListener("input", () => {

    if(confirmPassword.value === ""){

        confirmPassword.style.borderColor = "";

        return;

    }

    if(password.value === confirmPassword.value){

        confirmPassword.style.borderColor = "#22c55e";

    }

    else{

        confirmPassword.style.borderColor = "#ef4444";

    }

});

/*=======================================================
    VALIDATION DU FORMULAIRE
=======================================================*/

form.addEventListener("submit", (event) => {

    if(password.value !== confirmPassword.value){

        event.preventDefault();

        alert("Les mots de passe ne correspondent pas.");

        return;

    }

    if(password.value.length < 8){

        event.preventDefault();

        alert("Le mot de passe doit contenir au moins 8 caractères.");

        return;

    }

});



/*=======================================================
    ANIMATION DES CHAMPS
=======================================================*/

const inputs = document.querySelectorAll("input");

inputs.forEach(input => {

    input.addEventListener("focus", () => {

        input.parentElement.classList.add("active");

    });

    input.addEventListener("blur", () => {

        input.parentElement.classList.remove("active");

    });

});



/*=======================================================
    MESSAGE CONSOLE
=======================================================*/

console.log("ProjectStarter - Register chargé.");