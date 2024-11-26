class Shop:
    def __init__(self, id: int, name: str, login: str):
        self.id = id
        self.name = name
        self.login = login


class User:
    def __init__(self, id: int, name: str, login: str, balance: float):
        self.id = id
        self.name = name
        self.login = login
        self.balance = balance


class Category:
    def __init__(self, id: int, name: str):
        self.id = id
        self.name = name


class Product:
    def __init__(self, id: int, category: Category, shop: Shop, name: str, price: float, description: str):
        self.id = id
        self.category = category
        self.shop = shop
        self.name = name
        self.price = price
        self.description = description


class Paycheck:
    def __init__(self, id: int, user: User, products: list[Product], sum: float):
        self.id = id
        self.user = user
        self.products = products
        self.sum = sum


class ShoppingCart:
    def __init__(self, user: User, products: list[Product]):
        self.user = user
        self.products = products
