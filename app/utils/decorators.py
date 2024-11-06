from functools import wraps
from flask import request, current_app
from ..models.response import ApiResponse
from cachetools import TTLCache
import hashlib

# Cache for storing responses
response_cache = TTLCache(maxsize=100, ttl=300)

def validate_json(schema):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not request.is_json:
                return ApiResponse.error("Missing JSON in request", 400)
            
            errors = schema.validate(request.get_json())
            if errors:
                return ApiResponse.error("Validation error", 400, errors)
                
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def validate_file(allowed_extensions):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'file' not in request.files:
                return ApiResponse.error("No file part", 400)
                
            file = request.files['file']
            if file.filename == '':
                return ApiResponse.error("No selected file", 400)
                
            if not allowed_file(file.filename, allowed_extensions):
                return ApiResponse.error("File type not allowed", 400)
                
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def cache_response(timeout=300):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Create cache key from request data
            cache_key = hashlib.md5(
                f"{request.path}{str(request.get_json())}".encode()
            ).hexdigest()
            
            # Try to get response from cache
            cached_response = response_cache.get(cache_key)
            if cached_response is not None:
                return cached_response
            
            # Get fresh response
            response = f(*args, **kwargs)
            
            # Cache the response
            response_cache[cache_key] = response
            
            return response
        return decorated_function
    return decorator

def allowed_file(filename, allowed_extensions):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in allowed_extensions
