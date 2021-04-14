import os
import pytest
from flask import session
from app import app

@pytest.fixture
def url():
    url = 'http://127.0.0.1:3000'
    return url

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SECRET_KEY'] = os.urandom(24)
    client = app.test_client()
    return client

def test_index(url, client):
    res = client.get(url + '/')
    assert res.status_code == 200

def test_signup(url, client):
    res = client.post(url + '/signup', data=dict(name='test',username='test', password='test'))
    assert res.status_code == 302
    assert 'http://127.0.0.1:3000/error/?message=test&name=test' == res.headers['Location']

def test_signin_correct(url, client):
    res = client.post(url + '/signin', data=dict(username='test', password='test'))
    assert res.status_code == 302
    assert 'http://127.0.0.1:3000/member/' == res.headers['Location']

def test_signin_error(url, client):
    res = client.post(url + '/signin', data=dict(username='test', password='123'))
    assert res.status_code == 302
    assert 'http://127.0.0.1:3000/error/?message=test' == res.headers['Location']

def test_signout(url, client):
    res = client.get(url + '/signout')
    assert res.status_code == 302

def test_member_withSession(url, client):
    with client.session_transaction() as session:
        session['username'] = 'test'
        return session['username']
    assert client.get(url + '/member/').status_code == 200
    assert client.get(url + '/member/').headers['Location'] == 'http://127.0.0.1:3000/member/'

def test_member_withoutSession(url, client):
    res = client.get(url + '/member/')
    assert res.status_code == 302
    assert 'http://127.0.0.1:3000/' == res.headers['Location']

def test_error(url, client):
    res = client.get(url + '/error/')
    assert res.status_code == 200

def test_search_withSession(url, client):
    with client.session_transaction() as session:
        session['username'] = 'test'
        return session['username']
    assert client.get(url + '/api/users').status_code == 200
    assert client.get(url + '/api/users').data == b'{"data":{"id":1,"name":tester,"username":test}}\n'

def test_search_withoutSession(url, client):
    res = client.get(url + '/api/users')
    assert res.data == b'{"data":"null"}\n'

def test_update_withSession(url, client):
    import json
    data = {
        'name': 'tester'
    }
    headers = {
        'Content-Type': 'application/json'
    }
    with client.session_transaction() as session:
        session['username'] = 'test'
        return session['username']
    assert client.post(url + '/api/user', data=json.dumps(data), headers=headers).status_code == 200
    assert client.post(url + '/api/user', data=json.dumps(data),headers=headers).data == b'{"error":"same name error"}\n'

def test_update_withoutSession(url, client):
    import json
    data = {
        'name': 'tester'
    }
    headers = {
        'Content-Type': 'application/json'
    }
    res = client.post(url + '/api/user', data=json.dumps(data), headers=headers)
    assert res.status_code == 200
    assert res.get_data() == b'{"error":"database error"}\n'

