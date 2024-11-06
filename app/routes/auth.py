from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from marshmallow import Schema, fields, validate
from werkzeug.security import generate_password_hash, check_password_hash
import json

bp = Blueprint('auth', __name__)

# In-memory user store (replace with database in production)
USERS = {}

class UserSchema(Schema):
    username = fields.Str(required=True, validate=validate.Length(min=3, max=50))
    password = fields.Str(required=True, validate=validate.Length(min=6))

@bp.route('/api/v1/auth/register', methods=['POST'])
def register():
    schema = UserSchema()
    try:
        data = schema.load(request.get_json())
    except Exception as e:
        return jsonify({'error': str(e)}), 400
    
    if data['username'] in USERS:
        return jsonify({'error': 'Username already exists'}), 409
    
    # Hash password and store user
    hashed_password = generate_password_hash(data['password'])
    USERS[data['username']] = {
        'password': hashed_password
    }
    
    return jsonify({'message': 'User created successfully'}), 201

@bp.route('/api/v1/auth/login', methods=['POST'])
def login():
    schema = UserSchema()
    try:
        data = schema.load(request.get_json())
    except Exception as e:
        return jsonify({'error': str(e)}), 400
    
    user = USERS.get(data['username'])
    if not user or not check_password_hash(user['password'], data['password']):
        return jsonify({'error': 'Invalid credentials'}), 401
    
    # Create tokens
    access_token = create_access_token(identity=data['username'])
    refresh_token = create_refresh_token(identity=data['username'])
    
    return jsonify({
        'access_token': access_token,
        'refresh_token': refresh_token
    }), 200

@bp.route('/api/v1/auth/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    current_user = get_jwt_identity()
    new_access_token = create_access_token(identity=current_user)
    
    return jsonify({'access_token': new_access_token}), 200

@bp.route('/api/v1/auth/me', methods=['GET'])
@jwt_required()
def get_user():
    current_user = get_jwt_identity()
    return jsonify({'username': current_user}), 200
