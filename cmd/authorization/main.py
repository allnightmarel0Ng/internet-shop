import asyncio

from internal.config import load_config

from internal.infrastructure.postgres import Database
from internal.domain.repository import ShopRepository, UserRepository

from internal.app.authorization.repository import AuthorizationRepository
from internal.app.authorization.usecase import AuthorizationUseCase
from internal.app.authorization.handler import AuthorizationHandler

if __name__ == '__main__':
    config = load_config()

    db = Database(
        f"postgresql://{config.POSTGRES_USER}:{config.POSTGRES_PASSWORD}@postgres:{config.POSTGRES_PORT}/{config.POSTGRES_DB}")

    shop_repository = ShopRepository(db)
    user_repository = UserRepository(db)

    authorization_repository = AuthorizationRepository(
        shop_repository, user_repository)
    authorization_use_case = AuthorizationUseCase(
        authorization_repository, config.JWT_SECRET_KEY)
    authorization_handler = AuthorizationHandler(authorization_use_case)

    asyncio.run(authorization_handler.start(int(config.AUTHORIZATION_WS_PORT)))
