/*
======================================================
ProjectStarter
Version 1

BLOC 1

- Variables
- Ajout des pages
- Suppression
- Récupération des données

======================================================
*/





/*======================================================
                ELEMENTS HTML
======================================================*/

const form = document.getElementById("generator-form");

const projectNameInput = document.getElementById("project-name");

const pagesContainer = document.getElementById("pages-container");

const addPageButton = document.getElementById("add-page");

const preview = document.getElementById("project-preview");

const generateButton = document.getElementById("generate-button");





/*======================================================
                CASES A COCHER
======================================================*/

const htmlCheckbox = document.querySelector('[name="create_html"]');

const cssCheckbox = document.querySelector('[name="create_css"]');

const jsCheckbox = document.querySelector('[name="create_js"]');

const readmeCheckbox = document.querySelector('[name="create_readme"]');

const gitignoreCheckbox = document.querySelector('[name="create_gitignore"]');

const databaseCheckbox = document.querySelector('[name="create_database"]');

const requirementsCheckbox = document.querySelector('[name="create_requirements"]');

const configCheckbox = document.querySelector('[name="create_config"]');





/*======================================================
                CREATION D'UNE PAGE
======================================================*/

function createPageInput(value = "") {

    const row = document.createElement("div");

    row.className = "page-row";



    const input = document.createElement("input");

    input.type = "text";

    input.name = "pages";

    input.className = "page-input";

    input.placeholder = "home";

    input.value = value;



    const button = document.createElement("button");

    button.type = "button";

    button.className = "remove-page";

    button.innerHTML = "❌";



    row.appendChild(input);

    row.appendChild(button);



    pagesContainer.appendChild(row);

}





/*======================================================
            RECUPERATION DES PAGES
======================================================*/

function getPages() {

    const pages = [];



    document

        .querySelectorAll(".page-input")

        .forEach(input => {

            const value = input.value.trim();

            if (value !== "") {

                pages.push(value);

            }

        });



    return pages;

}





/*======================================================
            NETTOYAGE DES NOMS
======================================================*/

function cleanName(text) {

    return text

        .toLowerCase()

        .replace(/[^a-z0-9_-]/g, "");

}





/*======================================================
        AJOUT D'UNE PAGE
======================================================*/

addPageButton.addEventListener("click", () => {

    createPageInput("");

    updatePreview();

});





/*======================================================
        EVENEMENTS SUR LES INPUTS
======================================================*/

document.addEventListener("input", function (event) {

    if (event.target.classList.contains("page-input")) {

        event.target.value = cleanName(event.target.value);

        updatePreview();

    }



    if (event.target.id === "project-name") {

        event.target.value = cleanName(event.target.value);

        updatePreview();

    }

});





/*======================================================
        SUPPRESSION D'UNE PAGE
======================================================*/

document.addEventListener("click", function (event) {

    if (!event.target.classList.contains("remove-page")) {

        return;

    }



    const rows = document.querySelectorAll(".page-row");



    if (rows.length <= 1) {

        alert("Il faut au moins une page.");

        return;

    }



    event.target.parentElement.remove();

    updatePreview();

});





/*======================================================
        MISE A JOUR DES CHECKBOX
======================================================*/

document

.querySelectorAll('input[type="checkbox"]')

.forEach(box => {

    box.addEventListener(

        "change",

        updatePreview

    );

});

/*
======================================================
ProjectStarter
Version 1

BLOC 2

- Aperçu dynamique
- Gestion des options
- Mise à jour automatique

======================================================
*/





/*======================================================
                APERCU
======================================================*/

function updatePreview() {

    let projectName = projectNameInput.value.trim();

    if (projectName === "") {

        projectName = "MonProjet";

    }



    const pages = getPages();

    const projectType = document.querySelector(
        'input[name="project_type"]:checked'
    ).value;

    if(projectType === "flask"){

        configCheckbox.checked = true;
        requirementsCheckbox.checked = true;
        databaseCheckbox.checked = true;

        configCheckbox.disabled = true;
        requirementsCheckbox.disabled = true;
        databaseCheckbox.disabled = true;

    }else{

        configCheckbox.disabled = false;
        requirementsCheckbox.disabled = false;
        databaseCheckbox.disabled = false;

        configCheckbox.checked = false;
        requirementsCheckbox.checked = false;
        databaseCheckbox.checked = false;

    }

    let tree = "";



    tree += "📁 " + projectName + "\n\n";



    /*=========================================
                TEMPLATES
    =========================================*/

    if (htmlCheckbox.checked) {

        tree += "📁 templates\n";



        pages.forEach(page => {

            tree += "   📄 " + page + ".html\n";

        });



        tree += "\n";

    }



    /*=========================================
                STATIC
    =========================================*/

    tree += "📁 static\n";



    if (cssCheckbox.checked) {

        tree += "   📁 css\n";



        pages.forEach(page => {

            tree += "      🎨 " + page + ".css\n";

        });

    }



    if (jsCheckbox.checked) {

        tree += "\n";



        tree += "   📁 js\n";



        pages.forEach(page => {

            tree += "      ⚡ " + page + ".js\n";

        });

    }



    tree += "\n";

    /*=========================================
            FICHIERS DU PROJET
    =========================================*/

    if(projectType === "flask"){

        tree += "🚀 app.py\n";
        tree += "⚙️ config.py\n";
        tree += "🗄️ database.db\n";
        tree += "📦 requirements.txt\n";

    }else{

        if(databaseCheckbox.checked){

            tree += "🗄️ database.db\n";

        }

        if(configCheckbox.checked){

            tree += "⚙️ config.py\n";

        }

        if(requirementsCheckbox.checked){

            tree += "📦 requirements.txt\n";

        }

    }

    if (readmeCheckbox.checked) {

        tree += "📘 README.md\n";

    }



    if (gitignoreCheckbox.checked) {

        tree += "🙈 .gitignore\n";

    }



    preview.textContent = tree;

}



/*======================================================
            MISE A JOUR
======================================================*/

projectNameInput.addEventListener(

    "input",

    updatePreview

);



document.addEventListener(

    "input",

    function(event){

        if(event.target.classList.contains("page-input")){

            updatePreview();

        }

    }

);





/*======================================================
        CHECKBOX
======================================================*/

document

.querySelectorAll('input[type="checkbox"]')

.forEach(box=>{

    box.addEventListener(

        "change",

        updatePreview

    );

});

document
.querySelectorAll('input[name="project_type"]')
.forEach(radio => {

    radio.addEventListener(

        "change",

        updatePreview

    );

});





/*======================================================
        PREMIER AFFICHAGE
======================================================*/

window.addEventListener(

    "load",

    function(){

        updatePreview();

    }

);

/*
======================================================
ProjectStarter
Version 1

BLOC 3

- Validation
- Notifications
- Génération
- Initialisation

======================================================
*/





/*======================================================
                NOTIFICATIONS
======================================================*/

function showNotification(message, type = "success") {

    const old = document.querySelector(".notification");

    if (old) {

        old.remove();

    }

    const notification = document.createElement("div");

    notification.className = "notification";

    notification.textContent = message;

    notification.style.position = "fixed";
    notification.style.top = "25px";
    notification.style.right = "25px";
    notification.style.padding = "15px 22px";
    notification.style.borderRadius = "12px";
    notification.style.color = "white";
    notification.style.fontWeight = "600";
    notification.style.zIndex = "99999";
    notification.style.transition = ".3s";
    notification.style.opacity = "0";

    if (type === "error") {

        notification.style.background = "#DC2626";

    }

    else {

        notification.style.background = "#2563EB";

    }

    document.body.appendChild(notification);

    setTimeout(() => {

        notification.style.opacity = "1";

    }, 50);

    setTimeout(() => {

        notification.style.opacity = "0";

        setTimeout(() => {

            notification.remove();

        }, 300);

    }, 2500);

}





/*======================================================
            VALIDATION
======================================================*/

function validateForm() {

    const pages = getPages();



    if (projectNameInput.value.trim() === "") {

        showNotification(

            "Donne un nom au projet.",

            "error"

        );

        return false;

    }



    if (pages.length === 0) {

        showNotification(

            "Ajoute au moins une page.",

            "error"

        );

        return false;

    }



    const unique = new Set(pages);



    if (unique.size !== pages.length) {

        showNotification(

            "Deux pages portent le même nom.",

            "error"

        );

        return false;

    }



    if (

        !htmlCheckbox.checked &&

        !cssCheckbox.checked &&

        !jsCheckbox.checked

    ) {

        showNotification(

            "Choisis au moins un type de fichier.",

            "error"

        );

        return false;

    }



    return true;

}





/*======================================================
            ENVOI DU FORMULAIRE
======================================================*/

form.addEventListener("submit", async function(event){

    event.preventDefault();

    if(!validateForm()){

        return;

    }

    generateButton.disabled = true;
    generateButton.innerHTML = "⏳ Génération...";

    try{

        const response = await fetch(form.action,{

            method:"POST",

            body:new FormData(form)

        });

        if(!response.ok){

            throw new Error();

        }

        const blob = await response.blob();

        const url = window.URL.createObjectURL(blob);

        const link = document.createElement("a");

        link.href = url;

        link.download = "Projet.zip";

        document.body.appendChild(link);

        link.click();

        link.remove();

        window.URL.revokeObjectURL(url);

        showNotification("Projet généré avec succès !");

    }

    catch(error){

        showNotification(

            "Une erreur est survenue.",

            "error"

        );

    }

    finally{

        generateButton.disabled = false;

        generateButton.innerHTML = "🚀 Générer mon projet";

    }

});





/*======================================================
            ANIMATION DES INPUTS
======================================================*/

document.addEventListener("focusin", function (event) {

    if (event.target.classList.contains("page-input")) {

        event.target.style.transform = "scale(1.02)";

    }

});



document.addEventListener("focusout", function (event) {

    if (event.target.classList.contains("page-input")) {

        event.target.style.transform = "scale(1)";

    }

});





/*======================================================
        PREMIER CHARGEMENT
======================================================*/

window.addEventListener("DOMContentLoaded", () => {

    updatePreview();

    showNotification(

        "Bienvenue sur ProjectStarter 🚀"

    );

});