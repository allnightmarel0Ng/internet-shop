class SearchUseCase:
    def __init__(self, repository: SearchRepository):
        self.repository = repository

    async def search(self, query: str):
        if not query or not isinstance(query, str) or len(query.strip()) == 0:
            return []

        cleaned_query = query.strip()
        return await self.repository.search(cleaned_query)
