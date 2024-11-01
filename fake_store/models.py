from datetime import datetime
from typing import List, Literal

from pydantic import BaseModel, EmailStr, conint


class Categories(BaseModel):
    """
    Representa as categorias de produtos disponíveis.

    Args:
        category (List[Literal]): Lista de categorias válidas, incluindo
        "electronics", "jewelery", "men's clothing", "women's clothing".
    """

    category: List[
        Literal[
            "electronics", "jewelery", "men's clothing", "women's clothing"
        ]
    ]


class Product(BaseModel):
    """
    Representa um produto.

    Args:
        id (int): Identificador único do produto.
        title (str): Título do produto.
        price (float): Preço do produto.
        category (Literal): Categoria do produto, que pode ser
        "electronics", "jewelery", "men's clothing" ou "women's clothing".
        description (str): Descrição do produto.
        image (str): URL da imagem do produto.
    """

    id: int
    title: str
    price: float
    category: Literal[
        "electronics", "jewelery", "men's clothing", "women's clothing"
    ]
    description: str
    image: str


class ProductsInCart(BaseModel):
    """
    Representa um produto que está no carrinho.

    Args:
        productId (int): Identificador do produto.
        quantity (conint): Quantidade do produto, deve ser maior ou igual a 1.
    """

    productId: int
    quantity: conint(ge=1)


class Cart(BaseModel):
    """
    Representa o carrinho de compras de um usuário.

    Args:
        id (int): Identificador único do carrinho.
        userId (int): Identificador do usuário que possui o carrinho.
        date (datetime): Data em que o carrinho foi criado ou atualizado.
        products (List[ProductsInCart]): Lista de produtos no carrinho.
    """

    id: int
    userId: int
    date: datetime
    products: List[ProductsInCart]


class GeoLocation(BaseModel):
    """
    Representa a localização geográfica.

    Args:
        lat (str): Latitude.
        long (str): Longitude.
    """

    lat: str
    long: str


class Address(BaseModel):
    """
    Representa um endereço.

    Args:
        city (str): Nome da cidade.
        street (str): Nome da rua.
        number (int): Número do endereço.
        zipcode (str): Código postal.
        geolocation (GeoLocation): Localização geográfica do endereço.
    """

    city: str
    street: str
    number: int
    zipcode: str
    geolocation: GeoLocation


class Name(BaseModel):
    """
    Representa o nome de uma pessoa.

    Args:
        firstname (str): Primeiro nome.
        lastname (str): Sobrenome.
    """

    firstname: str
    lastname: str


class User(BaseModel):
    """
    Representa um único usuário.

    Args:
        id (int): Identificador único do usuário.
        email (EmailStr): Endereço de e-mail do usuário.
        username (str): Nome de usuário.
        password (str): Senha do usuário.
        name (Name): Nome completo do usuário.
        address (Address): Endereço do usuário.
        phone (str): Número de telefone do usuário.
    """

    id: int
    email: EmailStr
    username: str
    password: str
    name: Name
    address: Address
    phone: str
