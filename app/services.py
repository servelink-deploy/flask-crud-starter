from psycopg2.extras import RealDictCursor
from app.database import Database
from app.models import UserCreate, UserUpdate

class UserService:
    @staticmethod
    def create_user(user_data: UserCreate):
        with Database.get_connection() as conn:
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            cursor.execute(
                '''
                INSERT INTO users (name, email, phone)
                VALUES (%s, %s, %s)
                RETURNING id, name, email, phone, created_at, updated_at
                ''',
                (user_data.name, user_data.email, user_data.phone)
            )
            result = cursor.fetchone()
            cursor.close()
            return dict(result)
    
    @staticmethod
    def get_all_users(limit: int = 100, offset: int = 0):
        with Database.get_connection() as conn:
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            cursor.execute(
                '''
                SELECT id, name, email, phone, created_at, updated_at 
                FROM users 
                ORDER BY id DESC 
                LIMIT %s OFFSET %s
                ''',
                (limit, offset)
            )
            results = cursor.fetchall()
            
            cursor.execute('SELECT COUNT(*) as total FROM users')
            total = cursor.fetchone()['total']
            
            cursor.close()
            return {
                'users': [dict(row) for row in results],
                'total': total,
                'limit': limit,
                'offset': offset
            }
    
    @staticmethod
    def get_user_by_id(user_id: int):
        with Database.get_connection() as conn:
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            cursor.execute(
                'SELECT id, name, email, phone, created_at, updated_at FROM users WHERE id = %s',
                (user_id,)
            )
            result = cursor.fetchone()
            cursor.close()
            return dict(result) if result else None
    
    @staticmethod
    def search_users(query: str):
        with Database.get_connection() as conn:
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            search_pattern = f'%{query}%'
            cursor.execute(
                '''
                SELECT id, name, email, phone, created_at, updated_at 
                FROM users 
                WHERE name ILIKE %s OR email ILIKE %s
                ORDER BY id DESC
                LIMIT 50
                ''',
                (search_pattern, search_pattern)
            )
            results = cursor.fetchall()
            cursor.close()
            return [dict(row) for row in results]
    
    @staticmethod
    def update_user(user_id: int, user_data: UserUpdate):
        update_fields = []
        values = []
        
        if user_data.name is not None:
            update_fields.append('name = %s')
            values.append(user_data.name)
        
        if user_data.email is not None:
            update_fields.append('email = %s')
            values.append(user_data.email)
        
        if user_data.phone is not None:
            update_fields.append('phone = %s')
            values.append(user_data.phone)
        
        if not update_fields:
            return UserService.get_user_by_id(user_id)
        
        update_fields.append('updated_at = CURRENT_TIMESTAMP')
        values.append(user_id)
        
        with Database.get_connection() as conn:
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            query = f'''
                UPDATE users
                SET {', '.join(update_fields)}
                WHERE id = %s
                RETURNING id, name, email, phone, created_at, updated_at
            '''
            cursor.execute(query, values)
            result = cursor.fetchone()
            cursor.close()
            return dict(result) if result else None
    
    @staticmethod
    def delete_user(user_id: int):
        with Database.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM users WHERE id = %s RETURNING id', (user_id,))
            result = cursor.fetchone()
            cursor.close()
            return result is not None
