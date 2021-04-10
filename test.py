import pytest
import json
from app import app

@pytest.fixture
def url():
    url = 'http://127.0.0.1:3000'
    return url

@pytest.fixture
def client():
    client = app.test_client()
    return client

def test_index(url, client):
    res = client.get(url + '/')
    assert res.status_code == 200

def test_signup(url, client):
    res = client.post(url + '/signup', data=dict(name='test', username='test', password='test'))
    assert res.status_code == 302

def test_signin(url, client):
    res = client.post(url + '/signin', data=dict(username='test', password='test'))
    assert res.status_code == 302

def test_signout(url, client):
    res = client.get(url + '/signout')
    assert res.status_code == 302

def test_member(url, client):
    res = client.get(url + '/member/')
    assert res.status_code == 302

def test_error(url, client):
    res = client.get(url + '/error/')
    assert res.status_code == 200

def test_search(url, client):
    res = client.get(url + '/api/users')
    assert res.get_data() == b'{"data":"null"}\n'

def test_update(url, client):
    data = {
        'name': 'tester'
    }
    headers = {
        'Content-Type': 'application/json'
    }
    res = client.post(url + '/api/user', data=json.dumps(data), headers=headers)
    assert res.status_code == 200
    assert res.get_data() == b'{"error":"database error"}\n'

