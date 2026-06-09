import os


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "progym-dev-secret-key")

    DB_HOST = os.environ.get("DB_HOST", "localhost")
    DB_USER = os.environ.get("DB_USER", "root")
    DB_PASSWORD = os.environ.get("DB_PASSWORD", "")
    DB_NAME = os.environ.get("DB_NAME", "progym_gold_test")
    DB_PORT = int(os.environ.get("DB_PORT", 3307))