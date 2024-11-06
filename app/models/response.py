from flask import jsonify
from datetime import datetime

class ApiResponse:
    @staticmethod
    def success(data=None, message="Success"):
        response = {
            "status": "success",
            "message": message,
            "timestamp": datetime.utcnow().isoformat(),
            "data": data
        }
        return jsonify(response), 200

    @staticmethod
    def error(message, status_code=400, errors=None):
        response = {
            "status": "error",
            "message": message,
            "timestamp": datetime.utcnow().isoformat(),
            "errors": errors
        }
        return jsonify(response), status_code
