# Flaskie API

A powerful Flask REST API with advanced text processing, document handling, and image analysis capabilities.

## Features

- Rate limiting for API endpoints
- Environment variables configuration
- Text analysis using transformers
- Document processing (PDF, DOCX, XLSX, PPTX)
- Image processing and OCR
- Caching mechanisms
- PDF report generation
- Word cloud generation
- Secure API design

## Prerequisites

- Python 3.8+
- Virtual environment
- pip package manager

## Setting Up Development Environment

1. Create and activate virtual environment:

```bash
# On Windows
python -m venv venv
.\venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

2. Upgrade pip and install requirements:

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

## Project Structure

```
flaskie/
├── .env
├── .gitignore
├── requirements.txt
├── Procfile
├── runtime.txt
├── app/
│   ├── __init__.py
│   ├── config.py
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── documents.py
│   │   └── analysis.py
│   ├── models/
│   │   ├── __init__.py
│   │   └── response.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── text_processor.py
│   │   ├── doc_handler.py
│   │   └── image_analyzer.py
│   └── utils/
│       ├── __init__.py
│       ├── decorators.py
│       └── helpers.py
└── wsgi.py
```

## Environment Variables

Create a `.env` file in the root directory:

```env
FLASK_APP=wsgi.py
FLASK_ENV=development
SECRET_KEY=your-super-secret-key-change-in-production
RATE_LIMIT=100/hour
JWT_SECRET_KEY=another-super-secret-key-for-jwt
DATABASE_URL=sqlite:///flaskie.db
UPLOAD_FOLDER=uploads
MAX_CONTENT_LENGTH=16777216  # 16MB max file size
ALLOWED_EXTENSIONS=pdf,docx,xlsx,pptx,png,jpg,jpeg
```

## API Endpoints

### Authentication
- POST /api/v1/auth/register
- POST /api/v1/auth/login

### Document Processing
- POST /api/v1/documents/analyze
- POST /api/v1/documents/convert
- GET /api/v1/documents/{id}

### Text Analysis
- POST /api/v1/analysis/sentiment
- POST /api/v1/analysis/summary
- POST /api/v1/analysis/keywords

## Rate Limiting

The API implements rate limiting using Flask-Limiter:
- 100 requests per hour per IP
- 1000 requests per day per IP

## Deployment to Railway.com

1. Create a new project on Railway.com
2. Connect your GitHub repository
3. Set the following environment variables in Railway dashboard:
   - `FLASK_APP=wsgi.py`
   - `FLASK_ENV=production`
   - `SECRET_KEY=[your-secure-secret-key]`
   - `JWT_SECRET_KEY=[your-secure-jwt-key]`
   - `RATE_LIMIT=100/hour`
4. Deploy using Git:

```bash
git add .
git commit -m "Initial commit"
git push railway main
```

## Testing the API in your browser

Now, I'll provide you with instructions for testing the API in your browser using some dummy data:

1. First, register a user:

```bash
curl -X POST http://localhost:5000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser", "password":"testpass123"}'
```

2. Login to get an access token:

```bash
curl -X POST http://localhost:5000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser", "password":"testpass123"}'
```

3. Test the text analysis endpoint:

```bash
curl -X POST http://localhost:5000/api/v1/analysis/sentiment \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -d '{"text":"This is a great API service! I love using it."}'
```

4. Test document analysis (requires a PDF file):

```bash
curl -X POST http://localhost:5000/api/v1/documents/analyze \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -F "file=@/path/to/your/document.pdf"
```

## Flutter Integration

Here's a sample API service class for your Flutter app:

```dart
import 'dart:convert';
import 'package:http/http.dart' as http;
import 'package:firebase_auth/firebase_auth.dart';

class ApiService {
  static const String baseUrl = 'YOUR_RAILWAY_APP_URL';
  String? _accessToken;

  Future<String> _getAccessToken() async {
    // ...
  }

  Future<Map<String, dynamic>> analyzeSentiment(String text) async {
    // ...
  }

  Future<Map<String, dynamic>> analyzeDocument(List<int> fileBytes, String filename) async {
    // ...
  }
}
```

## Best Practices

1. **Security**
   - Use HTTPS in production
   - Implement rate limiting
   - Validate all input data
   - Use secure headers
   - Implement proper authentication

2. **Performance**
   - Implement caching
   - Use async operations where possible
   - Optimize database queries
   - Implement pagination

3. **Code Organization**
   - Follow modular architecture
   - Use blueprints for routes
   - Implement service layer
   - Use dependency injection

4. **Error Handling**
   - Use proper HTTP status codes
   - Return meaningful error messages
   - Log errors appropriately
   - Implement global error handling

5. **Documentation**
   - Document all endpoints
   - Provide example requests/responses
   - Include setup instructions
   - Document environment variables

## Testing

Run tests using pytest:

```bash
pytest tests/
```

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
