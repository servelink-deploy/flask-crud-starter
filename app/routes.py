from flask import Blueprint, request, jsonify
from pydantic import ValidationError
import psycopg2
from app.models import UserCreate, UserUpdate
from app.services import UserService
from app.database import Database
from app import limiter

health_bp = Blueprint('health', __name__)
users_bp = Blueprint('users', __name__)

@health_bp.route('/health', methods=['GET'])
def health_check():
    try:
        with Database.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT 1')
            cursor.close()
        return jsonify({
            'status': 'healthy',
            'database': 'connected',
            'service': 'flask-crud-api'
        }), 200
    except Exception as e:
        return jsonify({
            'status': 'unhealthy',
            'error': str(e)
        }), 500

@users_bp.route('/users', methods=['POST'])
@limiter.limit("10 per minute")
def create_user():
    try:
        user_data = UserCreate(**request.json)
        user = UserService.create_user(user_data)
        return jsonify({
            'message': 'Utilisateur créé avec succès',
            'data': user
        }), 201
    except ValidationError as e:
        return jsonify({
            'error': 'Erreur de validation',
            'details': e.errors()
        }), 400
    except psycopg2.IntegrityError:
        return jsonify({
            'error': 'Un utilisateur avec cet email existe déjà'
        }), 409
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@users_bp.route('/users', methods=['GET'])
def get_users():
    try:
        limit = request.args.get('limit', 100, type=int)
        offset = request.args.get('offset', 0, type=int)
        
        limit = min(limit, 100)
        
        result = UserService.get_all_users(limit, offset)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@users_bp.route('/users/search', methods=['GET'])
def search_users():
    try:
        query = request.args.get('q', '')
        if not query:
            return jsonify({'error': 'Paramètre de recherche "q" requis'}), 400
        
        users = UserService.search_users(query)
        return jsonify({
            'results': users,
            'count': len(users)
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@users_bp.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    try:
        user = UserService.get_user_by_id(user_id)
        if not user:
            return jsonify({'error': 'Utilisateur non trouvé'}), 404
        return jsonify(user), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@users_bp.route('/users/<int:user_id>', methods=['PUT'])
@limiter.limit("20 per minute")
def update_user(user_id):
    try:
        user_data = UserUpdate(**request.json)
        user = UserService.update_user(user_id, user_data)
        if not user:
            return jsonify({'error': 'Utilisateur non trouvé'}), 404
        return jsonify({
            'message': 'Utilisateur mis à jour avec succès',
            'data': user
        }), 200
    except ValidationError as e:
        return jsonify({
            'error': 'Erreur de validation',
            'details': e.errors()
        }), 400
    except psycopg2.IntegrityError:
        return jsonify({
            'error': 'Un utilisateur avec cet email existe déjà'
        }), 409
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@users_bp.route('/users/<int:user_id>', methods=['DELETE'])
@limiter.limit("10 per minute")
def delete_user(user_id):
    try:
        deleted = UserService.delete_user(user_id)
        if not deleted:
            return jsonify({'error': 'Utilisateur non trouvé'}), 404
        return jsonify({'message': 'Utilisateur supprimé avec succès'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
