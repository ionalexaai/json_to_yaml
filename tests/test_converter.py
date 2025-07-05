import multiprocessing
import time
import requests
import pytest

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import create_app

BASE_URL = "http://localhost:5000"


def run_app():
    """
    Runs the Flask app in a separate process using Gunicorn-style app factory
    """
    app = create_app()
    app.run(host="0.0.0.0", port=5000)


@pytest.fixture(scope="session", autouse=True)
def start_server():
    """
    Pytest fixture to start the server before tests and shut it down after
    """
    proc = multiprocessing.Process(target=run_app)
    proc.start()

    time.sleep(2)  # Give the server time to boot

    yield  # Run the tests

    proc.terminate()
    proc.join()


def test_homepage():
    response = requests.get(f"{BASE_URL}/")
    assert response.status_code == 200
    assert "Small converter API collection" in response.text


def test_json_to_yaml_conversion():
    payload = {
        "key": "value",
        "list": [1, 2, 3],
        "data": [{"key": "age"}, {"value": "old"}]
    }
    response = requests.post(f"{BASE_URL}/api/json_to_yaml", json=payload)

    assert response.status_code == 200
    assert "key: value" in response.text
    assert "list:" in response.text


def test_json_to_yaml_bad_json():
    bad_json = '{"key": "value", "list": [1, 2, 3], "data": [1, 2, 3],'  # Invalid JSON

    response = requests.post(
        f"{BASE_URL}/api/json_to_yaml",
        data=bad_json,
        headers={"Content-Type": "application/json"}
    )

    assert response.status_code == 400


def test_yaml_to_json_conversion():
    yaml_payload = """
    name: Alice
    skills:
      - Python
      - Docker
    """
    response = requests.post(
        f"{BASE_URL}/api/yaml_to_json",
        data=yaml_payload,
        headers={"Content-Type": "text/plain"}
    )

    assert response.status_code == 200
    json_data = response.json()
    assert json_data["name"] == "Alice"
    assert "skills" in json_data
    assert "Python" in json_data["skills"]
