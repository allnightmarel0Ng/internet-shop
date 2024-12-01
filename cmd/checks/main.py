from fastapi import FastAPI
import uvicorn

from internal.config import load_config
from internal.infrastructure.postgres import Database
from internal.domain.repository import CheckRepository

from internal.app.checks.usecase import CheckUseCase
from internal.app.checks.handler import CheckHandler

app = FastAPI()

@app.get('/')
async def hello():
    return 'pong'

if __name__ == '__main__':
    config = load_config()

    db = Database(
        f"postgresql://{config.POSTGRES_USER}:{config.POSTGRES_PASSWORD}@postgres:{config.POSTGRES_PORT}/{config.POSTGRES_DB}"
    )

    check_repository = CheckRepository(db)
    use_case = CheckUseCase(check_repository)
    handler = CheckHandler(use_case)

    app.include_router(handler.router)

    uvicorn.run(app, port=int(config.CHECKS_PORT), host="0.0.0.0")
