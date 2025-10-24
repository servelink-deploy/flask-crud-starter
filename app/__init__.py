from flask import Flask
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from app.config import Config
from app.database import Database

limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"],
    storage_uri="memory://"
)

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    CORS(app)
    limiter.init_app(app)
    
    with app.app_context():
        Database.init_db()
    
    from app.routes import users_bp, health_bp
    app.register_blueprint(health_bp)
    app.register_blueprint(users_bp, url_prefix='/api')
    
    from app.errors import register_error_handlers
    register_error_handlers(app)
    
    return app
