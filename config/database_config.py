# Database configuration
MYSQL_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'root@123',
    'database': 'medical_store',
}

from urllib.parse import quote_plus

password_encoded = quote_plus(MYSQL_CONFIG['password'])
# SQLAlchemy connection string
SQLALCHEMY_DATABASE_URL = f"mysql+mysqlconnector://{MYSQL_CONFIG['user']}:{password_encoded}@{MYSQL_CONFIG['host']}/{MYSQL_CONFIG['database']}"