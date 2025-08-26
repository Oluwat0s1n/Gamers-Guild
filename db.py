import os
from dotenv import load_dotenv
import mysql.connector

load_dotenv()  # reads .env at run time 

def get_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME"),
        port=int(os.getenv("DB_PORT", "3306"))
    )

def image_path(name: str) -> str:
    base = os.getenv("IMAGE_DIR", "images")  # default to 'images' folder
    return os.path.join(base, name)
