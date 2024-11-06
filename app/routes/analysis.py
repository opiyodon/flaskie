from flask import Blueprint, request
from flask_jwt_extended import jwt_required
from ..utils.decorators import validate_json, cache_response
from ..models.response import ApiResponse
from ..services.text_processor import analyze_sentiment, generate_summary, extract_keywords
from marshmallow import Schema, fields

analysis_bp = Blueprint('analysis', __name__)

class TextSchema(Schema):
    text = fields.Str(required=True)

@analysis_bp.route('/sentiment', methods=['POST'])
@jwt_required()
@validate_json(TextSchema())
@cache_response(timeout=300)
def sentiment_analysis():
    data = request.get_json()
    result = analyze_sentiment(data['text'])
    return ApiResponse.success(result)

@analysis_bp.route('/summary', methods=['POST'])
@jwt_required()
@validate_json(TextSchema())
@cache_response(timeout=300)
def text_summary():
    data = request.get_json()
    result = generate_summary(data['text'])
    return ApiResponse.success(result)

@analysis_bp.route('/keywords', methods=['POST'])
@jwt_required()
@validate_json(TextSchema())
@cache_response(timeout=300)
def keyword_extraction():
    data = request.get_json()
    result = extract_keywords(data['text'])
    return ApiResponse.success(result)
