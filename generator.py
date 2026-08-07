"""
=========================================================
ProjectStarter

generator.py

BLOC 1

- Classe principale
- Initialisation
- Création du dossier principal
- Méthode generate()

=========================================================
"""

from pathlib import Path
import textwrap


class ProjectGenerator:

    def __init__(
        self,
        project_name,
        project_type,
        pages,

        create_html,
        create_css,
        create_js,

        create_readme,
        create_gitignore,
        create_database,
        create_config,
        create_requirements
    ):

        # --------------------------------------
        # Informations du projet
        # --------------------------------------

        self.project_name = project_name.strip()

        self.project_type = project_type

        self.pages = pages

        # --------------------------------------
        # Options
        # --------------------------------------

        self.create_html = create_html

        self.create_css = create_css

        self.create_js = create_js

        self.create_readme = create_readme

        self.create_gitignore = create_gitignore

        self.create_database = create_database

        self.create_config = create_config

        self.create_requirements = create_requirements

        # --------------------------------------
        # Dossiers
        # --------------------------------------

        self.generated_projects = Path("generated_projects")

        self.project_folder = (
            self.generated_projects / self.project_name
        )

        self.templates_folder = (
            self.project_folder / "templates"
        )

        self.static_folder = (
            self.project_folder / "static"
        )

        self.css_folder = (
            self.static_folder / "css"
        )

        self.js_folder = (
            self.static_folder / "js"
        )


    # =====================================================
    # Création du projet
    # =====================================================

    def generate(self):

        """
        Fonction principale.

        Elle sera complétée dans les blocs suivants.
        """

        # Création du dossier principal

        self.project_folder.mkdir(
            parents=True,
            exist_ok=True
        )

        if self.project_type == "flask":
            self.create_config = True
            self.create_requirements = True
            self.create_database = True

        # Création de l'arborescence

        self.create_structure()

        # Création des pages

        self.create_pages()

        # Fichiers supplémentaires

        self.create_extra_files()

        # Si le projet est de type Flask,
        # on ajoute les fichiers spécifiques.

        if self.project_type == "flask":

            self.create_flask_files()

        return self.project_folder


    # =====================================================
    # Création de l'arborescence
    # =====================================================

    def create_structure(self):

        """
        Crée les dossiers nécessaires.
        """

        if self.create_html:

            self.templates_folder.mkdir(
                parents=True,
                exist_ok=True
            )

        self.static_folder.mkdir(
            parents=True,
            exist_ok=True
        )

        if self.create_css:

            self.css_folder.mkdir(
                parents=True,
                exist_ok=True
            )

        if self.create_js:

            self.js_folder.mkdir(
                parents=True,
                exist_ok=True
            )



    # =====================================================
    # Création des pages
    # =====================================================

    def create_pages(self):

        """
        Crée tous les fichiers HTML, CSS et JS.
        """

        for page in self.pages:

            self.create_html_file(page)

            self.create_css_file(page)

            self.create_js_file(page)



    # =====================================================
    # HTML
    # =====================================================

    def create_html_file(self, page):

        if not self.create_html:

            return

        html_file = self.templates_folder / f"{page}.html"

        html_file.write_text(
f"""<!DOCTYPE html>
<html lang="fr">

<head>

    <meta charset="UTF-8">

    <title>{page}</title>

    <link rel="stylesheet"
          href="../static/css/{page}.css">

</head>

<body>

    <h1>{page}</h1>

    <script src="../static/js/{page}.js"></script>

</body>

</html>
""",
encoding="utf-8"
        )



    # =====================================================
    # CSS
    # =====================================================

    def create_css_file(self, page):

        if not self.create_css:

            return

        css_file = self.css_folder / f"{page}.css"

        css_file.write_text(
f"""/*

======================================

{page}.css

Créé automatiquement par ProjectStarter

======================================

*/

body {{

    margin:0;

    padding:0;

    font-family:Arial,sans-serif;

}}

""",
encoding="utf-8"
        )



    # =====================================================
    # JS
    # =====================================================

    def create_js_file(self, page):

        if not self.create_js:

            return

        js_file = self.js_folder / f"{page}.js"

        js_file.write_text(
f"""/*

======================================

{page}.js

Créé automatiquement par ProjectStarter

======================================

*/

console.log("{page} chargé.");

""",
encoding="utf-8"
        )


    # =====================================================
    # FICHIERS SUPPLEMENTAIRES
    # =====================================================

    def create_extra_files(self):

        """
        Création des fichiers optionnels.
        """

        if self.create_readme:

            self.create_readme_file()

        if self.create_gitignore:

            self.create_gitignore_file()

        if self.create_database:

            self.create_database_file()

        if self.create_config:

            self.create_config_file()

        if self.create_requirements:

            self.create_requirements_file()



    # =====================================================
    # README.md
    # =====================================================

    def create_readme_file(self):

        readme = self.project_folder / "README.md"

        readme.write_text(
f"""# {self.project_name}

Projet créé automatiquement avec ProjectStarter.

## Structure

- templates/
- static/css/
- static/js/

Bon développement 🚀
""",
encoding="utf-8"
        )



    # =====================================================
    # .gitignore
    # =====================================================

    def create_gitignore_file(self):

        gitignore = self.project_folder / ".gitignore"

        gitignore.write_text(
"""__pycache__/
*.pyc
.venv/
.env
""",
encoding="utf-8"
        )



    # =====================================================
    # database.db
    # =====================================================

    def create_database_file(self):

        database = self.project_folder / "database.db"

        database.touch(exist_ok=True)



    # =====================================================
    # config.py
    # =====================================================

    def create_config_file(self):

        config = self.project_folder / "config.py"

        config.write_text(
"""SECRET_KEY = "change_me"

DEBUG = True
""",
encoding="utf-8"
        )



    # =====================================================
    # requirements.txt
    # =====================================================

    def create_requirements_file(self):

        requirements = self.project_folder / "requirements.txt"

        requirements.write_text(
"""Flask
""",
encoding="utf-8"
        )

    # =====================================================
    # FLASK
    # =====================================================

    def create_flask_files(self):

        app_file = self.project_folder / "app.py"

        app_file.write_text(
            textwrap.dedent(
                f"""\
        from flask import Flask, render_template

        app = Flask(__name__)


        @app.route("/")
        def home():
            return render_template("{self.pages[0]}.html")


        if __name__ == "__main__":
            app.run(
                debug=True,
                host="127.0.0.1",
                port=5000
            )
        """
            ),
            encoding="utf-8"
        )

        config_file = self.project_folder / "config.py"

        config_file.write_text(
            '''SECRET_KEY = "CHANGE_ME"
        
            DEBUG = True
            ''',
            encoding="utf-8"
        )

        requirements = self.project_folder / "requirements.txt"

        requirements.write_text(
            '''Flask
            ''',
            encoding="utf-8"
        )

        database = self.project_folder / "database.db"

        database.touch(exist_ok=True)