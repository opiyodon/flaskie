import pytest
from app import create_app
from flask import json

@pytest.fixture
def app():
    app = create_app()
    app.config['TESTING'] = True
    return app

@pytest.fixture
def client(app):
    return app.test_client()

def test_register(client):
    response = client.post('/api/v1/auth/register',
        json={
            'username': 'testuser',
            'password': 'testpass123'
        }
    )
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['status'] == 'success'

def test_login(client):
    # First register a user
    client.post('/api/v1/auth/register',
        json={
            'username': 'testuser',
            'password': 'testpass123'
        }
    )
    
    # Then try to login
    response = client.post('/api/v1/auth/login',
        json={
            'username': 'testuser',
            'password': 'testpass123'
        }
    )
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['status'] == 'success'
    assert 'access_token' in data['data']

def test_invalid_login(client):
    response = client.post('/api/v1/auth/login',
        json={
            'username': 'wronguser',
            'password': 'wrongpass'
        }
    )
    assert response.status_code == 401
