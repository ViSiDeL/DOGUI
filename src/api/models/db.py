"""
db connection
"""
import os
import pymysql
from typing import Any, Dict

def get_connection():
    """
    create and return a new DB connection from env vars
    """
    conn = pymysql.connect(
        host=os.getenv('DB_HOST', 'localhost'),
        user=os.getenv('DB_USER', ''),
        password=os.getenv('DB_PASSWORD', ''),
        database=os.getenv('DB_DATABASE', ''),
        port=int(os.getenv('DB_PORT', 3306))
    )
    conn.autocommit(True)
    return conn