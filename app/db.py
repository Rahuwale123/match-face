import mysql.connector
from mysql.connector import Error
import os

def get_db_config():
    """Return hardcoded database configuration"""
    return {
        'host': 'localhost',
        'user': 'root',
        'password': 'QWer12@*',
        'database': 'face_recognition_db'
    }

def get_db_connection():
    """Create and return a database connection"""
    try:
        config = get_db_config()
        connection = mysql.connector.connect(
            host=config['host'],
            user=config['user'],
            password=config['password'],
            database=config['database']
        )
        return connection
    except Error as e:
        print(f"Error while connecting to MySQL: {e}")
        raise

def init_db():
    """Initialize the database with the faces table"""
    try:
        config = get_db_config()
        connection = mysql.connector.connect(
            host=config['host'],
            user=config['user'],
            password=config['password']
        )
        
        cursor = connection.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {config['database']}")
        cursor.execute(f"USE {config['database']}")
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS faces (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id VARCHAR(255) NOT NULL,
                name VARCHAR(255) NOT NULL,
                embedding TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        connection.commit()
        cursor.close()
        connection.close()
    except Error as e:
        print(f"Error while initializing MySQL database: {e}")
        raise