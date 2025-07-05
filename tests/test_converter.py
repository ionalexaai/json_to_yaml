import requests

def test_homepage():
    response = requests.get('http://localhost:3000')
    assert 'Small converter API collection' in response.text

def test_converter():

    payload = {"key": "value", "list": [1, 2, 3], "data": [{"key": "age"}, {"value": "old"}]}
    response = requests.post('http://localhost:3000/api/json_to_yaml', json=payload)

    assert 'key: value' in response.text