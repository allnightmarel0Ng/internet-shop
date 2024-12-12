class SearchRepository:
    def __init__(self, db: Database):
        self.__shop_repo = ShopRepository(db)
        self.__category_repo = CategoryRepository(db)
        self.__product_repo = ProductRepository(db)

    def search(self, query: str) -> dict:

        shops = self.__shop_repo.search_shops(query)

        categories = self.__category_repo.search_categories(query)

        products = self.__product_repo.search_products(query)

        return {
            "shops": shops,
            "categories": categories,
            "products": products
        }
