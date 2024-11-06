from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from ..services.text_processor import TextProcessor
from marshmallow import Schema, fields

bp = Blueprint('analysis', __name__)
text_processor = TextProcessor()

class TextAnalysisSchema(Schema):
    text = fields.Str(required=True)

@bp.route('/api/v1/analysis/sentiment', methods=['POST'])
@jwt_required()
def analyze_sentiment():
    schema = TextAnalysisSchema()
    try:
        data = schema.load(request.get_json())
    except Exception as e:
        return jsonify({'error': str(e)}), 400
    
    result = text_processor.analyze_sentiment(data['text'])
    return jsonify(result)

@bp.route('/api/v1/analysis/summary', methods=['POST'])
@jwt_required()
def generate_summary():
    schema = TextAnalysisSchema()
    try:
        data = schema.load(request.get_json())
    except Exception as e:
        return jsonify({'error': str(e)}), 400
    
    result = text_processor.generate_summary(data['text'])
    return jsonify(result)

@bp.route('/api/v1/analysis/keywords', methods=['POST'])
@jwt_required()
def extract_keywords():
    schema = TextAnalysisSchema()
    try:
        data = schema.load(request.get_json())
    except Exception as e:
        return jsonify({'error': str(e)}), 400
    
    result = text_processor.extract_keywords(data['text'])
    return jsonify(result)
