from fastapi import APIRouter, Query

class SearchHandler:
    def __init__(self, use_case: SearchUseCase):
        self.router = APIRouter()
        self.use_case = use_case

        @self.router.get("/search")
        async def search(query: str = Query(..., description="The search bar")):
            results = await self.use_case.search(query)
            return {"query": query, "results": results}
