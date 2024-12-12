class SearchUseCase:
    def __init__(self, repository: SearchRepository):
        self.repository = repository

    async def search(self, query: str) -> dict:
        return self.repository.search(query)
