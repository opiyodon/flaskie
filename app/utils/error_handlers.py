from flask import jsonify
from werkzeug.exceptions import HTTPException
from ..models.response import ApiResponse

def register_error_handlers(app):
    @app.errorhandler(400)
    def bad_request(e):
        return ApiResponse.error("Bad request", 400)

    @app.errorhandler(401)
    def unauthorized(e):
        return ApiResponse.error("Unauthorized", 401)

    @app.errorhandler(403)
    def forbidden(e):
        return ApiResponse.error("Forbidden", 403)

    @app.errorhandler(404)
    def not_found(e):
        return ApiResponse.error("Resource not found", 404)

    @app.errorhandler(405)
    def method_not_allowed(e):
        return ApiResponse.error("Method not allowed", 405)

    @app.errorhandler(429)
    def too_many_requests(e):
        return ApiResponse.error("Too many requests", 429)

    @app.errorhandler(500)
    def internal_server_error(e):
        return ApiResponse.error("Internal server error", 500)

    @app.errorhandler(HTTPException)
    def handle_http_exception(e):
        return ApiResponse.error(e.description, e.code)

    @app.errorhandler(Exception)
    def handle_generic_exception(e):
        return ApiResponse.error(str(e), 500)
