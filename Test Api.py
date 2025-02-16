import pytest
import requests
import random

BASE_URL = "https://qa-internship.avito.com/api/1"

@pytest.fixture
def seller_id():
    return random.randint(111111, 999999)

@pytest.fixture
def item_payload(seller_id):
    return {
        "sellerID": seller_id,
        "name": "Тестовый товар",
        "price": 100,
        "statistics": {
            "contacts": 5,
            "likes": 10,
            "viewCount": 20
        }
    }

@pytest.fixture
def created_item(item_payload):
    response = requests.post(f"{BASE_URL}/item", json=item_payload)
    assert response.status_code == 200
    return response.json()["id"]

# Создания объявления
def test_create_item_valid(item_payload):
    response = requests.post(f"{BASE_URL}/item", json=item_payload)
    assert response.status_code == 200
    assert "id" in response.json()

def test_create_item_without_seller():
    payload = {"name": "Тест", "price": 100}
    response = requests.post(f"{BASE_URL}/item", json=payload)
    assert response.status_code == 400

def test_create_item_invalid_seller():
    payload = {"sellerID": 1000, "name": "Тест", "price": 100}
    response = requests.post(f"{BASE_URL}/item", json=payload)
    assert response.status_code == 400

def test_create_item_negative_price():
    payload = {"sellerID": 123456, "name": "Тест", "price": -100}
    response = requests.post(f"{BASE_URL}/item", json=payload)
    assert response.status_code == 400

# Получения объявления
def test_get_existing_item(created_item):
    response = requests.get(f"{BASE_URL}/item/{created_item}")
    assert response.status_code == 200

def test_get_non_existent_item():
    response = requests.get(f"{BASE_URL}/item/00000000-0000-0000-0000-000000000000")
    assert response.status_code == 404

# Получения объявлений по sellerID
def test_get_items_by_seller(seller_id):
    response = requests.get(f"{BASE_URL}/{seller_id}/item")
    assert response.status_code == 200

def test_get_items_by_invalid_seller():
    response = requests.get(f"{BASE_URL}/000000/item")
    assert response.status_code == 400

# Получение статистики
def test_get_statistics_for_existing_item(created_item):
    response = requests.get(f"{BASE_URL}/statistic/{created_item}")
    assert response.status_code == 200

def test_get_statistics_for_non_existent_item():
    response = requests.get(f"{BASE_URL}/statistic/00000000-0000-0000-0000-000000000000")
    assert response.status_code == 404
