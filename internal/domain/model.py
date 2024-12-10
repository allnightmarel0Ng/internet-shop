import datetime


class Shop:
    def __init__(self, shop_id: int, name: str, login: str):
        self.id = shop_id
        self.name = name
        self.login = login


class User:
    def __init__(self, user_id: int, name: str, login: str, balance: float):
        self.id = user_id
        self.name = name
        self.login = login
        self.balance = balance


class Category:
    def __init__(self, category_id: int, name: str):
        self.id = category_id
        self.name = name


class Product:
    def __init__(self, product_id: int, category_id: int, shop_id: int, name: str, price: float):
        self.id = product_id
        self.category_id = category_id
        self.shop_id = shop_id
        self.name = name
        self.price = price


class Paycheck:
    def __init__(self, paycheck_id: int, user_id: int, total_price: float, creation_time: datetime.time):
        self.id = paycheck_id
        self.user_id = user_id
        self.total_price = total_price
        self.creation_time = creation_time

class PaycheckItem:
    def __init__(self, paycheck_item_id: int, paycheck_id: int, product_id: int):
        self.id = paycheck_item_id
        self.paycheck_id = paycheck_id
        self.product_id = product_id


class ShoppingCart:
    def __init__(self, shopping_cart_id: int, user_id: int, product_id: int):
        self.id = shopping_cart_id
        self.user_id = user_id
        self.product_id = product_id
