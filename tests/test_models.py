from datetime import datetime

import pytest
from pydantic import ValidationError

from fake_store.models import (
    Address,
    Cart,
    Categories,
    GeoLocation,
    Name,
    Product,
    ProductsInCart,
    User,
)


def test_categories_valid():
    data = {"category": ["electronics", "jewelery"]}
    categories = Categories(**data)
    assert categories.category == ["electronics", "jewelery"]


def test_categories_invalid():
    data = {"category": ["invalid_category"]}
    with pytest.raises(ValidationError):
        Categories(**data)


def test_product_valid():
    data = {
        "id": 1,
        "title": "Laptop",
        "price": 1200.50,
        "category": "electronics",
        "description": "A powerful laptop",
        "image": "https://example.com/laptop.png",
    }
    product = Product(**data)
    assert product.id == 1
    assert product.title == "Laptop"
    assert product.price == data.get("price")


def test_product_invalid_category():
    data = {
        "id": 1,
        "title": "Laptop",
        "price": 1200.50,
        "category": "invalid_category",
        "description": "A powerful laptop",
        "image": "https://example.com/laptop.png",
    }
    with pytest.raises(ValidationError):
        Product(**data)


def test_products_in_cart_valid():
    data = {"productId": 1, "quantity": 2}
    product_in_cart = ProductsInCart(**data)
    assert product_in_cart.productId == data.get("productId")
    assert product_in_cart.quantity == data.get("quantity")


def test_products_in_cart_invalid_quantity():
    data = {"productId": 1, "quantity": -1}
    with pytest.raises(ValidationError):
        ProductsInCart(**data)


def test_cart_valid():
    data = {
        "id": 1,
        "userId": 1,
        "date": datetime.now(),
        "products": [{"productId": 1, "quantity": 2}],
    }
    cart = Cart(**data)
    assert cart.id == 1
    assert cart.userId == 1
    assert len(cart.products) == 1
    assert cart.products[0].productId == 1


def test_cart_invalid_date():
    data = {
        "id": 1,
        "userId": 1,
        "date": "invalid_date",
        "products": [{"productId": 1, "quantity": 2}],
    }
    with pytest.raises(ValidationError):
        Cart(**data)


def test_geolocation_valid():
    data = {"lat": "45.0", "long": "90.0"}
    geolocation = GeoLocation(**data)
    assert geolocation.lat == "45.0"
    assert geolocation.long == "90.0"


def test_geolocation_invalid():
    data = {"lat": 45.0, "long": 90.0}  # Inteiros ao invés de strings
    with pytest.raises(ValidationError):
        GeoLocation(**data)


def test_address_valid():
    data = {
        "city": "New York",
        "street": "5th Ave",
        "number": 10,
        "zipcode": "10001",
        "geolocation": {"lat": "45.0", "long": "90.0"},
    }
    address = Address(**data)
    assert address.city == "New York"
    assert address.street == "5th Ave"
    assert address.number == data.get("number")
    assert address.zipcode == "10001"


def test_address_invalid_zipcode():
    data = {
        "city": "New York",
        "street": "5th Ave",
        "number": 10,
        "zipcode": 10001,  # Deve ser string
        "geolocation": {"lat": "45.0", "long": "90.0"},
    }
    with pytest.raises(ValidationError):
        Address(**data)


def test_name_valid():
    data = {"firstname": "John", "lastname": "Doe"}
    name = Name(**data)
    assert name.firstname == "John"
    assert name.lastname == "Doe"


def test_name_invalid():
    data = {"firstname": 123, "lastname": "Doe"}
    with pytest.raises(ValidationError):
        Name(**data)


def test_user_valid():
    data = {
        "id": 1,
        "email": "user@example.com",
        "username": "username",
        "password": "securepassword",
        "name": {"firstname": "John", "lastname": "Doe"},
        "address": {
            "city": "New York",
            "street": "5th Ave",
            "number": 10,
            "zipcode": "10001",
            "geolocation": {"lat": "45.0", "long": "90.0"},
        },
        "phone": "123-456-7890",
    }
    user = User(**data)
    assert user.id == 1
    assert user.email == "user@example.com"
    assert user.username == "username"


def test_user_invalid_email():
    data = {
        "id": 1,
        "email": "invalid_email",
        "username": "username",
        "password": "securepassword",
        "name": {"firstname": "John", "lastname": "Doe"},
        "address": {
            "city": "New York",
            "street": "5th Ave",
            "number": 10,
            "zipcode": "10001",
            "geolocation": {"lat": "45.0", "long": "90.0"},
        },
        "phone": "123-456-7890",
    }
    with pytest.raises(ValidationError):
        User(**data)
