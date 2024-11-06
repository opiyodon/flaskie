# Flaskie API

A powerful Flask REST API with advanced text processing, document handling, and image analysis capabilities.

## Features

- JWT Authentication
- Sentiment Analysis using transformers
- Rate limiting for API endpoints
- Environment variables configuration
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

## API Testing Guide

### 1. User Registration

Request:
```bash
curl -X POST http://localhost:5000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser", "password":"testpass123"}'
```

Response:
```json
{
    "data": "User registered successfully",
    "message": "Success",
    "status": "success",
    "timestamp": "2024-11-06T20:23:34.135271"
}
```

### 2. User Login

Request:
```bash
curl -X POST http://localhost:5000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser", "password":"testpass123"}'
```

Response:
```json
{
    "data": {
        "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
        "token_type": "bearer"
    },
    "message": "Success",
    "status": "success",
    "timestamp": "2024-11-06T20:24:00.013003"
}
```

### 3. Sentiment Analysis

Request:
```bash
curl -X POST http://localhost:5000/api/v1/analysis/sentiment \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -d '{"text":"This is a great API service! I love using it."}'
```

Response:
```json
{
    "data": {
        "confidence": 0.9996,
        "sentiment": "POSITIVE"
    },
    "message": "Success",
    "status": "success",
    "timestamp": "2024-11-06T20:46:53.265900"
}
```

### 4. Text Analysis Examples

Here are some example texts you can use to test the sentiment analysis endpoint:

Positive Examples:
```json
{
    "text": "This product exceeds all my expectations! Absolutely wonderful!"
}
```

```json
{
    "text": "The customer service team was incredibly helpful and responsive."
}
```

Negative Examples:
```json
{
    "text": "This service is terrible, I'm very disappointed with the results."
}
```

```json
{
    "text": "The interface is confusing and the documentation is unclear."
}
```

### 5. Document Analysis

Request:
```bash
curl -X POST http://localhost:5000/api/v1/documents/analyze \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -F "file=@sample.txt"
```

Sample test files you can create:

1. Create `sample.txt`:
```bash
echo "This is a sample document for testing the document analysis endpoint. 
It contains multiple sentences and paragraphs.
The API should be able to analyze this content and provide meaningful insights." > sample.txt
```

2. Create `test.pdf` (requires `pandoc`):
```bash
echo "# Test Document
This is a PDF document created for testing purposes.
It contains formatted text that can be analyzed by the API." | pandoc -f markdown -o test.pdf
```

## Rate Limiting

The API implements rate limiting:
- 100 requests per hour per IP
- 1000 requests per day per IP

## Error Handling

Common error responses:

```json
{
    "error": "Invalid credentials",
    "message": "Failed",
    "status": "error",
    "timestamp": "2024-11-06T20:47:00.000000"
}
```

```json
{
    "error": "Token has expired",
    "message": "Failed",
    "status": "error",
    "timestamp": "2024-11-06T20:47:00.000000"
}
```

## Deployment to Railway.com

1. Create a new project on Railway.com
2. Connect your GitHub repository
3. Set environment variables in Railway dashboard
4. Deploy using Git:

```bash
git add .
git commit -m "Initial commit"
git push railway main
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.