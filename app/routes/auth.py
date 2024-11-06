from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from ..utils.decorators import validate_json
from ..models.response import ApiResponse
from marshmallow import Schema, fields, validate
import hashlib

auth_bp = Blueprint('auth', __name__)

class UserSchema(Schema):
    username = fields.Str(required=True, validate=validate.Length(min=3, max=50))
    password = fields.Str(required=True, validate=validate.Length(min=6))

# Dummy user database (replace with real database in production)
users_db = {}

@auth_bp.route('/register', methods=['POST'])
@validate_json(UserSchema())
def register():
    data = request.get_json()
    username = data['username']
    
    if username in users_db:
        return ApiResponse.error("Username already exists", 400)
    
    # Hash password (use proper password hashing in production)
    password_hash = hashlib.sha256(data['password'].encode()).hexdigest()
    users_db[username] = password_hash
    
    return ApiResponse.success("User registered successfully")

@auth_bp.route('/login', methods=['POST'])
@validate_json(UserSchema())
def login():
    data = request.get_json()
    username = data['username']
    password_hash = hashlib.sha256(data['password'].encode()).hexdigest()
    
    if username not in users_db or users_db[username] != password_hash:
        return ApiResponse.error("Invalid credentials", 401)
    
    access_token = create_access_token(identity=username)
    return ApiResponse.success({
        "access_token": access_token,
        "token_type": "bearer"
    })

@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def get_user_profile():
    current_user = get_jwt_identity()
    return ApiResponse.success({
        "username": current_user
    })
