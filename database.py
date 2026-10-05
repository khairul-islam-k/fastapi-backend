import pymysql
from pymysql.cursors import DictCursor
import os
from dotenv import load_dotenv

def get_database_connection():
    conn = pymysql.connect(
        host= os.getenv("DB_HOST", "localhost"),
        user= os.getenv("DB_USER", "root"),
        password= os.getenv("DB_PASSWORD", ""),
        database= os.getenv("DB_NAME", ""),
        cursorclass=DictCursor,
    )
    return conn