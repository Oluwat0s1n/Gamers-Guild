import os
from dotenv import load_dotenv
import mysql.connector

load_dotenv()  # reads .env when you run locally

def get_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME"),
        port=int(os.getenv("DB_PORT", "3306"))
    )

def image_path(filename: str) -> str:
    base = os.getenv("IMAGE_DIR", "images")
    return os.path.join(base, filename)
