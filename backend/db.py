import mysql.connector
from mysql.connector import Error
from config import MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DATABASE

def get_db_connection():
    """Establish a connection to the MySQL database."""
    try:
        connection = mysql.connector.connect(
            host=MYSQL_HOST,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD,
            database=MYSQL_DATABASE
        )
        return connection
    except Error as e:
        print(f"Error: Could not connect to MySQL - {e}")
        return None  # Return None instead of crashing the app

def initialize_db():
    """Create necessary database tables if they do not exist."""
    db = get_db_connection()
    if db is None:
        print("Database connection failed. Skipping initialization.")
        return

    cursor = db.cursor()
    
    # Create documents table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS documents (
        doc_id VARCHAR(36) PRIMARY KEY,  -- Unique document ID
        filename VARCHAR(255) UNIQUE NOT NULL,
        content LONGTEXT NOT NULL
    )
    """)

    # Create document embeddings table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS document_embeddings (
        doc_id VARCHAR(36),
        embedding BLOB NOT NULL,
        FOREIGN KEY (doc_id) REFERENCES documents(doc_id) ON DELETE CASCADE
    )
    """)

    db.commit()
    cursor.close()
    db.close()
    print("Database initialized successfully.")

# Initialize database on startup
initialize_db()
