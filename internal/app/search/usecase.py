class SearchUseCase:
    def __init__(self, repository: SearchRepository):
        self.repository = repository

    async def search(self, query: str) -> dict:

        if not query or not isinstance(query, str) or len(query.strip()) == 0:
            return []
        
        query_like = query.strip().replace(" ", "%")

        return await self.repository.search(query_like)
