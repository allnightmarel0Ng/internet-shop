from fastapi import APIRouter, Depends, Header, HTTPException
from internal.app.checks.usecase import CheckUseCase

class CheckHandler:
    def __init__(self, use_case: CheckUseCase):
        self.router = APIRouter()
        self.use_case = use_case

        @self.router.get("/checks")
        async def get_checks(auth: str = Header(None)):
            if not auth:
                raise HTTPException(status_code=401, detail="Auth header missing")
            try:
                return await self.use_case.get_checks(auth)
            except Exception as e:
                raise HTTPException(status_code=401, detail=str(e))
