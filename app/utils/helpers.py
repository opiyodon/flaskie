from functools import wraps
from flask import jsonify, request
import time
import logging

def measure_time(f):
    """Decorator to measure the execution time of a function."""
    @wraps(f)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = f(*args, **kwargs)
        end = time.time()
        logging.info(f'{f.__name__} took {end - start:.2f} seconds to execute')
        return result
    return wrapper

def validate_json(schema_class):
    """Decorator to validate JSON input using marshmallow schema."""
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            schema = schema_class()
            try:
                data = schema.load(request.get_json())
            except Exception as e:
                return jsonify({'error': str(e)}), 400
            return f(*args, **kwargs, validated_data=data)
        return wrapper
    return decorator

def cache_response(timeout=300):
    """Decorator to cache response for a specified time."""
    def decorator(f):
        cache = {}
        @wraps(f)
        def wrapper(*args, **kwargs):
            key = str(args) + str(kwargs)
            if key in cache:
                result, timestamp = cache[key]
                if time.time() - timestamp < timeout:
                    return result
            result = f(*args, **kwargs)
            cache[key] = (result, time.time())
            return result
        return wrapper
    return decorator

def error_handler(f):
    """Decorator to handle errors in a consistent way."""
    @wraps(f)
    def wrapper(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            logging.error(f'Error in {f.__name__}: {str(e)}')
            return jsonify({
                'error': 'Internal server error',
                'message': str(e)
            }), 500
    return wrapper
