from flask import Flask, render_template, request, send_file, redirect, session, flash
from pathlib import Path

from generator import ProjectGenerator
from zip_manager import ZipManager

from database import DatabaseManager

from flask import abort

from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash

from datetime import datetime

from shutil import copy2

import os

app = Flask(__name__)
app.secret_key = "CLE_SECRETE_HUGO_APP"

@app.after_request
def add_no_cache_headers(response):

    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"

    response.headers["Pragma"] = "no-cache"

    response.headers["Expires"] = "0"

    return response

database = DatabaseManager()

# Création automatique des dossiers utiles
Path("temp").mkdir(exist_ok=True)
Path("generated_projects").mkdir(exist_ok=True)
Path("storage").mkdir(exist_ok=True)

Path("storage/zips").mkdir(parents=True, exist_ok=True)


@app.route("/")
def index():
    """
    Affiche la page principale.
    """
    return render_template("index.html")


@app.route("/generate", methods=["POST"])
def generate():

    if "user_id" not in session:

        return redirect("/login")

    # --------------------------
    # Récupération des données
    # --------------------------

    project_name = request.form.get("project_name", "").strip()

    project_type = request.form.get("project_type", "html")

    pages = request.form.getlist("pages")

    pages = [

        page.strip()

        for page in pages

        if page.strip()

    ]

    # --------------------------
    # Options
    # --------------------------

    create_html = "create_html" in request.form
    create_css = "create_css" in request.form
    create_js = "create_js" in request.form

    create_readme = "create_readme" in request.form
    create_gitignore = "create_gitignore" in request.form
    create_database = "create_database" in request.form
    create_config = "create_config" in request.form
    create_requirements = "create_requirements" in request.form

    # --------------------------
    # Génération
    # --------------------------
    print(project_type)

    generator = ProjectGenerator(
        project_name=project_name,
        project_type=project_type,
        pages=pages,

        create_html=create_html,
        create_css=create_css,
        create_js=create_js,

        create_readme=create_readme,
        create_gitignore=create_gitignore,
        create_database=create_database,
        create_config=create_config,
        create_requirements=create_requirements,
    )

    project_folder = generator.generate()

    # --------------------------
    # ZIP
    # --------------------------

    zip_manager = ZipManager(project_folder)

    zip_file = zip_manager.create_zip()

    # --------------------------
    # Sauvegarde du projet
    # --------------------------

    database.create_project(

        user_id=session["user_id"],

        project_name=project_name,

        project_type=project_type,

        zip_name=Path(zip_file).name,

        created_at=datetime.now().strftime("%d/%m/%Y %H:%M")

    )

    last_project = database.get_last_project()

    project_id = last_project[0]

    user_folder = Path(

        "storage",

        "zips",

        str(session["user_id"])

    )

    user_folder.mkdir(

        parents=True,

        exist_ok=True

    )

    destination = user_folder / Path(zip_file).name

    copy2(

        zip_file,

        destination

    )

    database.update_zip_path(

        project_id,

        str(destination)

    )

    # --------------------------
    # Téléchargement
    # --------------------------

    return send_file(
        zip_file,
        as_attachment=True,
        download_name=f"{project_name}.zip"
    )


@app.route("/download/<int:project_id>")
def download_project(project_id):

    if "user_id" not in session:

        return redirect("/login")

    projects = database.get_projects(

        session["user_id"]

    )

    for project in projects:

        if project[0] == project_id:
            return send_file(

                project[4],

                as_attachment=True,

                download_name=f"{project[1]}.zip"

            )

    return "Projet introuvable."



@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "GET":

        return render_template("register.html")


    username = request.form.get("username", "").strip()

    email = request.form.get("email", "").strip().lower()

    password = request.form.get("password", "")

    confirm_password = request.form.get("confirm_password", "")


    # Vérification des champs

    if not username or not email or not password:

        return "Tous les champs sont obligatoires."


    if password != confirm_password:
        flash(

            "Les mots de passe ne correspondent pas.",

            "error"

        )

        return redirect("/register")


    if len(password) < 8:

        return "Le mot de passe doit contenir au moins 8 caractères."


    # Hash du mot de passe

    hashed_password = generate_password_hash(password)


    try:

        database.create_user(

            username,

            email,

            hashed_password

        )

    except Exception:

        flash(

            "Ce nom d'utilisateur ou cette adresse e-mail est déjà utilisée.",

            "error"

        )

        return redirect("/register")

    flash(

        "Compte créé avec succès. Vous pouvez maintenant vous connecter.",

        "success"

    )

    return redirect("/login")

@app.route("/login", methods=["GET", "POST"])
def login():

    # --------------------------
    # Affichage de la page
    # --------------------------

    if request.method == "GET":

        return render_template("login.html")


    # --------------------------
    # Données du formulaire
    # --------------------------

    email = request.form.get("email", "").strip().lower()

    password = request.form.get("password", "")


    # --------------------------
    # Recherche utilisateur
    # --------------------------

    user = database.get_user_by_email(email)

    if user is None:
        flash(

            "Adresse e-mail ou mot de passe incorrect.",

            "error"

        )

        return redirect("/login")


    # --------------------------
    # Vérification du mot de passe
    # --------------------------

    if not check_password_hash(user[3], password):
        flash(

            "Adresse e-mail ou mot de passe incorrect.",

            "error"

        )

        return redirect("/login")


    # --------------------------
    # Création de la session
    # --------------------------

    session["user_id"] = user[0]

    session["username"] = user[1]

    session["is_admin"] = user[6]


    # --------------------------
    # Redirection
    # --------------------------

    return redirect("/dashboard")

@app.route("/dashboard")
def dashboard():

    if "user_id" not in session:

        abort(401)


    projects = database.get_projects(

        session["user_id"]

    )


    project_count = database.count_user_projects(

        session["user_id"]

    )


    return render_template(

        "dashboard.html",

        username=session["username"],

        projects=projects,

        project_count=project_count

    )

@app.route("/admin")
def admin_dashboard():

    # ----------------------------------
    # Vérification connexion
    # ----------------------------------

    if "user_id" not in session:

        return redirect("/login")


    # ----------------------------------
    # Vérification administrateur
    # ----------------------------------

    if session.get("is_admin") != 1:

        return redirect("/")


    # ----------------------------------
    # Statistiques
    # ----------------------------------

    total_users = database.count_users()

    total_projects = database.count_projects()


    return render_template(

        "admin/dashboard.html",

        total_users=total_users,

        total_projects=total_projects

    )

@app.route("/admin/users")
def admin_users():

    if "user_id" not in session:

        return redirect("/login")

    if session.get("is_admin") != 1:

        return redirect("/")

    return render_template("admin/users.html")

@app.route("/admin/projects")
def admin_projects():

    if "user_id" not in session:

        return redirect("/login")

    if session.get("is_admin") != 1:

        return redirect("/")

    return render_template("admin/projects.html")




@app.route("/logout")
def logout():

    session.clear()

    return redirect("/")

@app.route("/delete_project/<int:project_id>")
def delete_project(project_id):

    if "user_id" not in session:

        return redirect("/login")


    projects = database.get_projects(session["user_id"])

    for project in projects:

        if project[0] == project_id:

            zip_path = project[4]

            if zip_path and os.path.exists(zip_path):

                os.remove(zip_path)

            database.delete_project(

                project_id,

                session["user_id"]

            )

            break


    return redirect("/dashboard")

@app.route("/pricing")
def pricing():

    return render_template("pricing.html")

@app.route("/documentation")
def documentation():

    return render_template("documentation.html")

# =====================================
# Pages d'erreur
# =====================================

@app.errorhandler(401)
def error_401(error):

    return render_template("401.html"), 401


@app.errorhandler(403)
def error_403(error):

    return render_template("403.html"), 403


@app.errorhandler(404)
def error_404(error):

    return render_template("404.html"), 404


@app.errorhandler(500)
def error_500(error):

    return render_template("500.html"), 500

if __name__ == "__main__":
    app.run(
        debug=True,
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 8000))
    )