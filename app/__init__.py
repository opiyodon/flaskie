from flask import Flask, Blueprint
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from .config import Config
from .routes import register_routes
from . import auth, documents, analysis

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions
    CORS(app)
    JWTManager(app)
    limiter = Limiter(
        app=app,
        key_func=get_remote_address,
        default_limits=["100 per hour", "1000 per day"]
    )

    # Register routes
    register_routes(app)

    @app.route('/health')
    def health_check():
        return {'status': 'healthy'}, 200

    return app

def register_routes(app):
    """Register all blueprints/routes with the app."""
    
    # Register blueprints
    app.register_blueprint(auth.bp)
    app.register_blueprint(documents.bp)
    app.register_blueprint(analysis.bp)
    
    # Register error handlers
    register_error_handlers(app)

def register_error_handlers(app):
    """Register error handlers for common HTTP errors."""
    
    @app.errorhandler(400)
    def bad_request(e):
        return {'error': 'Bad request', 'message': str(e)}, 400

    @app.errorhandler(401)
    def unauthorized(e):
        return {'error': 'Unauthorized', 'message': str(e)}, 401

    @app.errorhandler(403)
    def forbidden(e):
        return {'error': 'Forbidden', 'message': str(e)}, 403

    @app.errorhandler(404)
    def not_found(e):
        return {'error': 'Not found', 'message': str(e)}, 404

    @app.errorhandler(405)
    def method_not_allowed(e):
        return {'error': 'Method not allowed', 'message': str(e)}, 405

    @app.errorhandler(429)
    def too_many_requests(e):
        return {'error': 'Too many requests', 'message': str(e)}, 429

    @app.errorhandler(500)
    def internal_server_error(e):
        return {'error': 'Internal server error', 'message': str(e)}, 500
