import requests
import random
import pytest

BASE_URL = "https://qa-internship.avito.com"

@pytest.fixture
def unique_seller_id():
    return random.randint(111111, 999999)

@pytest.fixture
def test_advert(unique_seller_id):
    payload = {
        "title": "Test Advert",
        "description": "Test Description",
        "price": 100,
        "seller_id": unique_seller_id
    }
    response = requests.post(f"{BASE_URL}/adverts", json=payload)
    assert response.status_code == 201
    return response.json()["id"], unique_seller_id

def test_create_advert(unique_seller_id):
    payload = {
        "title": "Test Advert",
        "description": "Test Description",
        "price": 100,
        "seller_id": unique_seller_id
    }
    response = requests.post(f"{BASE_URL}/adverts", json=payload)
    assert response.status_code == 201
    assert "id" in response.json()

def test_get_advert(test_advert):
    advert_id, _ = test_advert
    response = requests.get(f"{BASE_URL}/adverts/{advert_id}")
    assert response.status_code == 200
    assert response.json()["id"] == advert_id

def test_get_adverts_by_seller(test_advert):
    _, seller_id = test_advert
    response = requests.get(f"{BASE_URL}/adverts?seller_id={seller_id}")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_stats(test_advert):
    advert_id, _ = test_advert
    response = requests.get(f"{BASE_URL}/stats/{advert_id}")
    assert response.status_code == 200

def test_get_nonexistent_advert():
    response = requests.get(f"{BASE_URL}/adverts/99999999")
    assert response.status_code == 404
