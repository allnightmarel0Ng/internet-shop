class SearchUseCase:
    def __init__(self, repository: SearchRepository):
        self.repository = repository

    async def search(self, query: str) -> dict:

        if not query or not isinstance(query, str) or len(query.strip()) == 0:
            return []

        query_words = query.strip().split()

        query_like_conditions = [f"%{word}%" for word in query_words]

        return await self.repository.search(query_like_conditions)
