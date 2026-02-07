import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_hello(client):
    """Test the root route returns correct greeting."""
    rv = client.get('/')
    assert b"Hello form Docker!" in rv.data
