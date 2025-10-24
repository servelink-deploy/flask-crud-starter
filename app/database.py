import psycopg2
from psycopg2.extras import RealDictCursor
from contextlib import contextmanager
from app.config import Config

class Database:
    @staticmethod
    @contextmanager
    def get_connection():
        conn = None
        try:
            conn = psycopg2.connect(Config.DATABASE_URL)
            yield conn
            conn.commit()
        except Exception as e:
            if conn:
                conn.rollback()
            raise e
        finally:
            if conn:
                conn.close()
    
    @staticmethod
    def init_db():
        with Database.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(255) NOT NULL,
                    email VARCHAR(255) UNIQUE NOT NULL,
                    phone VARCHAR(50),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            cursor.execute('''
                CREATE INDEX IF NOT EXISTS idx_users_email ON users(email)
            ''')
            cursor.close()
