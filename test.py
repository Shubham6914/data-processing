from utils.db_handler import engine
import mysql.connector
from config.database_config import MYSQL_CONFIG,SQLALCHEMY_DATABASE_URL

def test_sqlalchemy_connection():
    try:
        with engine.connect() as connection:
            print("SQLAlchemy Connection Successful!")
            connection.close()
    except Exception as e:
        print(f"SQLAlchemy Connection Failed: {e}")

def test_mysql_connector():
    try:
        conn = mysql.connector.connect(**MYSQL_CONFIG)
        if conn.is_connected():
            print("MySQL Connector Connection Successful!")
            conn.close()
    except Exception as e:
        print(f"MySQL Connector Connection Failed: {e}")

if __name__ == "__main__":
    test_sqlalchemy_connection()
    test_mysql_connector()