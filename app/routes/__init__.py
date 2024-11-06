from .auth import auth_bp
from .documents import documents_bp
from .analysis import analysis_bp

__all__ = [
    'auth_bp',
    'documents_bp',
    'analysis_bp'
]