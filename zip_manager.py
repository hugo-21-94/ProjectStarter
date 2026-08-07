"""
=========================================================
ProjectStarter

zip_manager.py

Gestion de la création des archives ZIP

=========================================================
"""

from pathlib import Path
import zipfile


class ZipManager:

    def __init__(self, project_folder):

        """
        project_folder : chemin du projet généré
        """

        self.project_folder = Path(project_folder)

        self.zip_path = self.project_folder.with_suffix(".zip")


    # =====================================================
    # Création du ZIP
    # =====================================================

    def create_zip(self):

        """
        Crée une archive ZIP du projet.

        Retourne le chemin du fichier ZIP.
        """

        # Supprime l'ancien ZIP s'il existe
        if self.zip_path.exists():

            self.zip_path.unlink()


        # Création du ZIP
        with zipfile.ZipFile(

            self.zip_path,

            "w",

            compression=zipfile.ZIP_DEFLATED

        ) as zip_file:


            # Parcours de tous les fichiers du projet
            for file in self.project_folder.rglob("*"):

                # On ignore les dossiers
                if file.is_dir():

                    continue


                # Chemin dans le ZIP
                arcname = file.relative_to(
                    self.project_folder
                )


                # Ajout au ZIP
                zip_file.write(

                    file,

                    arcname=arcname

                )


        return self.zip_path