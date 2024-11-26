from fastapi import FastAPI
import uvicorn

from internal.config import load_config

from internal.infrastructure.postgres import Database
from internal.domain.repository import ShopRepository, UserRepository

from internal.app.authorization.repository import AuthorizationRepository
from internal.app.authorization.usecase import AuthorizationUseCase
from internal.app.authorization.handler import AuthorizationHandler

app = FastAPI()
@app.get('/')
async def hello():
    return 'pong'

if __name__ == '__main__':
    config = load_config()

    db = Database(
        f"postgresql://{config.POSTGRES_USER}:{config.POSTGRES_PASSWORD}@postgres:{config.POSTGRES_PORT}/{config.POSTGRES_DB}")

    shop_repository = ShopRepository(db)
    user_repository = UserRepository(db)

    repository = AuthorizationRepository(
        shop_repository, user_repository)
    use_case = AuthorizationUseCase(
        repository, config.JWT_SECRET_KEY)
    handler = AuthorizationHandler(use_case)
    
    app.include_router(handler.router)

    uvicorn.run(app, port=int(config.AUTHORIZATION_PORT), host="0.0.0.0")
