from fastapi import APIRouter
from pydantic import BaseModel

class SearchRequest(BaseModel):
    query: str

class SearchHandler:
    def __init__(self, use_case: SearchUseCase):
        self.router = APIRouter()
        self.use_case = use_case

        @self.router.post("/search")
        async def search(request: SearchRequest):
            results = self.use_case.search(request.query)
            return {"query": request.query, "results": results}
