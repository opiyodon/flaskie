from typing import Any, Optional, Dict, List
from dataclasses import dataclass
import json

@dataclass
class APIResponse:
    """Standard API response model."""
    success: bool
    data: Optional[Any] = None
    message: Optional[str] = None
    errors: Optional[List[Dict[str, str]]] = None
    meta: Optional[Dict[str, Any]] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert response to dictionary."""
        response = {
            'success': self.success
        }
        
        if self.data is not None:
            response['data'] = self.data
            
        if self.message is not None:
            response['message'] = self.message
            
        if self.errors is not None:
            response['errors'] = self.errors
            
        if self.meta is not None:
            response['meta'] = self.meta
            
        return response

    def to_json(self) -> str:
        """Convert response to JSON string."""
        return json.dumps(self.to_dict())

    @classmethod
    def success_response(cls, 
                        data: Optional[Any] = None, 
                        message: Optional[str] = None,
                        meta: Optional[Dict[str, Any]] = None) -> 'APIResponse':
        """Create a success response."""
        return cls(
            success=True,
            data=data,
            message=message,
            meta=meta
        )

    @classmethod
    def error_response(cls,
                      message: str,
                      errors: Optional[List[Dict[str, str]]] = None,
                      meta: Optional[Dict[str, Any]] = None) -> 'APIResponse':
        """Create an error response."""
        return cls(
            success=False,
            message=message,
            errors=errors,
            meta=meta
        )

    @classmethod
    def validation_error(cls,
                        errors: List[Dict[str, str]],
                        message: str = "Validation error") -> 'APIResponse':
        """Create a validation error response."""
        return cls(
            success=False,
            message=message,
            errors=errors
        )
