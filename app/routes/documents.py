from flask import Blueprint, request
from flask_jwt_extended import jwt_required
from werkzeug.utils import secure_filename
from ..utils.decorators import validate_file
from ..models.response import ApiResponse
from ..services.doc_handler import process_document
import os

documents_bp = Blueprint('documents', __name__)

@documents_bp.route('/analyze', methods=['POST'])
@jwt_required()
@validate_file(['pdf', 'docx', 'xlsx', 'pptx'])
def analyze_document():
    if 'file' not in request.files:
        return ApiResponse.error("No file provided", 400)
    
    file = request.files['file']
    if file.filename == '':
        return ApiResponse.error("No selected file", 400)
    
    filename = secure_filename(file.filename)
    filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)
    
    try:
        result = process_document(filepath)
        return ApiResponse.success(result)
    except Exception as e:
        return ApiResponse.error(str(e), 500)
    finally:
        # Clean up uploaded file
        if os.path.exists(filepath):
            os.remove(filepath)

@documents_bp.route('/<string:doc_id>', methods=['GET'])
@jwt_required()
def get_document(doc_id):
    # Dummy response for testing
    return ApiResponse.success({
        "id": doc_id,
        "name": f"Document_{doc_id}",
        "type": "pdf",
        "created_at": "2024-03-20T10:00:00Z",
        "status": "processed"
    })
