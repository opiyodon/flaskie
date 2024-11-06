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
SECRET_KEY=your-secret-key
RATE_LIMIT=100/hour
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
3. Set environment variables in Railway dashboard
4. Deploy using the following commands:

```bash
git add .
git commit -m "Initial commit"
git push railway main
```

## Integration with Flutter and Firebase

### Flutter Integration

1. Add HTTP package to your Flutter project:

```yaml
dependencies:
  http: ^0.13.5
```

2. Create an API service class:

```dart
class FlaskieAPI {
  static const String baseUrl = 'your-railway-app-url';
  
  Future<dynamic> analyzeSentiment(String text) async {
    final response = await http.post(
      Uri.parse('$baseUrl/api/v1/analysis/sentiment'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({'text': text}),
    );
    
    if (response.statusCode == 200) {
      return jsonDecode(response.body);
    } else {
      throw Exception('Failed to analyze sentiment');
    }
  }
  
  // Add other API methods here
}
```

### Firebase Integration

1. Set up Firebase Authentication in your Flutter app
2. Pass Firebase ID token to Flask API:

```dart
Future<String> getIdToken() async {
  final user = FirebaseAuth.instance.currentUser;
  return await user?.getIdToken() ?? '';
}

Future<dynamic> makeAuthenticatedRequest() async {
  final token = await getIdToken();
  final response = await http.get(
    Uri.parse('$baseUrl/api/v1/protected-endpoint'),
    headers: {
      'Authorization': 'Bearer $token',
      'Content-Type': 'application/json',
    },
  );
  return jsonDecode(response.body);
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
