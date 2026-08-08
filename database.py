"""
=========================================================
ProjectStarter

database.py

Gestion de la base de données PostgreSQL

=========================================================
"""

import os
import psycopg


class DatabaseManager:

    def __init__(self):

        self.database_url = os.environ.get("DATABASE_URL")

        if not self.database_url:

            raise RuntimeError(
                "DATABASE_URL n'est pas configurée."
            )

        self.create_database()


    # =====================================================
    # Connexion
    # =====================================================

    def connect(self):

        return psycopg.connect(
            self.database_url
        )


    # =====================================================
    # Création des tables
    # =====================================================

    def create_database(self):

        connection = self.connect()

        cursor = connection.cursor()


        # ============================================
        # USERS
        # ============================================

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (

            id SERIAL PRIMARY KEY,

            username TEXT UNIQUE NOT NULL,

            email TEXT UNIQUE NOT NULL,

            password TEXT NOT NULL,

            is_premium INTEGER DEFAULT 0,

            projects_created INTEGER DEFAULT 0,

            is_admin INTEGER DEFAULT 0,

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

            last_login TEXT

        )
        """)


        # ============================================
        # PROJECTS
        # ============================================

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS projects (

            id SERIAL PRIMARY KEY,

            user_id INTEGER NOT NULL,

            project_name TEXT NOT NULL,

            project_type TEXT NOT NULL,

            zip_name TEXT,

            created_at TEXT,

            FOREIGN KEY(user_id)
                REFERENCES users(id)
                ON DELETE CASCADE

        )
        """)


        connection.commit()

        cursor.close()

        connection.close()


    # =====================================================
    # Création d'un utilisateur
    # =====================================================

    def create_user(
        self,
        username,
        email,
        password
    ):

        connection = self.connect()

        cursor = connection.cursor()

        cursor.execute(
            """
            INSERT INTO users (

                username,

                email,

                password

            )

            VALUES (%s, %s, %s)
            """,

            (
                username,
                email,
                password
            )

        )

        connection.commit()

        cursor.close()

        connection.close()


    # =====================================================
    # Recherche d'un utilisateur par email
    # =====================================================

    def get_user_by_email(self, email):

        connection = self.connect()

        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT *

            FROM users

            WHERE email = %s
            """,

            (email,)

        )

        user = cursor.fetchone()

        cursor.close()

        connection.close()

        return user


    # =====================================================
    # Création d'un projet
    # =====================================================

    def create_project(

        self,

        user_id,

        project_name,

        project_type,

        zip_name,

        created_at

    ):

        connection = self.connect()

        cursor = connection.cursor()

        cursor.execute(
            """

            INSERT INTO projects (

                user_id,

                project_name,

                project_type,

                zip_name,

                created_at

            )

            VALUES (%s, %s, %s, %s, %s)

            """,

            (

                user_id,

                project_name,

                project_type,

                zip_name,

                created_at

            )

        )

        connection.commit()

        cursor.close()

        connection.close()


    # =====================================================
    # Récupération des projets d'un utilisateur
    # =====================================================

    def get_projects(self, user_id):

        connection = self.connect()

        cursor = connection.cursor()

        cursor.execute(
            """

            SELECT *

            FROM projects

            WHERE user_id = %s

            ORDER BY id DESC

            """,

            (user_id,)

        )

        projects = cursor.fetchall()

        cursor.close()

        connection.close()

        return projects


    # =====================================================
    # Nombre de projets d'un utilisateur
    # =====================================================

    def count_user_projects(self, user_id):

        connection = self.connect()

        cursor = connection.cursor()

        cursor.execute(
            """

            SELECT COUNT(*)

            FROM projects

            WHERE user_id = %s

            """,

            (user_id,)

        )

        total = cursor.fetchone()[0]

        cursor.close()

        connection.close()

        return total


    # =====================================================
    # Mise à jour du chemin du ZIP
    # =====================================================

    def update_zip_path(

        self,

        project_id,

        zip_path

    ):

        connection = self.connect()

        cursor = connection.cursor()

        cursor.execute(
            """

            UPDATE projects

            SET zip_name = %s

            WHERE id = %s

            """,

            (

                zip_path,

                project_id

            )

        )

        connection.commit()

        cursor.close()

        connection.close()


    # =====================================================
    # Dernier projet créé
    # =====================================================

    def get_last_project(self):

        connection = self.connect()

        cursor = connection.cursor()

        cursor.execute(
            """

            SELECT id

            FROM projects

            ORDER BY id DESC

            LIMIT 1

            """

        )

        project = cursor.fetchone()

        cursor.close()

        connection.close()

        return project


    # =====================================================
    # Supprimer un projet
    # =====================================================

    def delete_project(

        self,

        project_id,

        user_id

    ):

        connection = self.connect()

        cursor = connection.cursor()

        cursor.execute(
            """

            DELETE FROM projects

            WHERE id = %s

            AND user_id = %s

            """,

            (

                project_id,

                user_id

            )

        )

        connection.commit()

        cursor.close()

        connection.close()


    # =====================================================
    # Nombre d'utilisateurs
    # =====================================================

    def count_users(self):

        connection = self.connect()

        cursor = connection.cursor()

        cursor.execute(
            "SELECT COUNT(*) FROM users"
        )

        total = cursor.fetchone()[0]

        cursor.close()

        connection.close()

        return total


    # =====================================================
    # Nombre de projets
    # =====================================================

    def count_projects(self):

        connection = self.connect()

        cursor = connection.cursor()

        cursor.execute(
            "SELECT COUNT(*) FROM projects"
        )

        total = cursor.fetchone()[0]

        cursor.close()

        connection.close()

        return total


    # =====================================================
    # Mettre un utilisateur administrateur
    # =====================================================

    def make_admin_by_id(self, user_id):

        connection = self.connect()

        cursor = connection.cursor()

        cursor.execute(
            """

            UPDATE users

            SET is_admin = 1

            WHERE id = %s

            """,

            (user_id,)

        )

        connection.commit()

        updated = cursor.rowcount

        cursor.close()

        connection.close()

        return updated