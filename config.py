import os

# Config class that always reads from current env
class Config:
    @staticmethod
    def get_admin_username():
        return os.getenv("ADMIN_USERNAME")

    @staticmethod
    def get_admin_password_hash():
        return os.getenv("ADMIN_PASSWORD_HASH")

    @staticmethod
    def get_secret_key():
        return os.getenv("FLASK_SECRET_KEY")

    @staticmethod
    def get_database_path():
        return os.getenv("DATABASE_PATH", "database/portfolio.db")

    @staticmethod
    def get_debug():
        return os.getenv("FLASK_DEBUG", "False") == "True"

    
    @staticmethod
    def get_api_key():
        return os.getenv("API_SECRET_KEY")