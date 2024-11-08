import asyncio

from internal.config.config import load_config

from internal.infrastructure.postgres.database import Database
from internal.domain.repository.shop import ShopRepository
from internal.domain.repository.user import UserRepository

from internal.app.authorization.repository import AuthorizationRepository
from internal.app.authorization.usecase import AuthorizationUseCase
from internal.app.authorization.handler import AuthorizationHandler

if __name__ == '__main__':
    config = load_config()

    db = Database(
        f"postgresql://{config.postgres_user}:{config.postgres_password}@postgres:{config.postgres_port}/{config.postgres_db}")

    shop_repository = ShopRepository(db)
    user_repository = UserRepository(db)

    authorization_repository = AuthorizationRepository(
        shop_repository, user_repository)
    authorization_use_case = AuthorizationUseCase(
        authorization_repository, config.jwt_secret_key)
    authorization_handler = AuthorizationHandler(authorization_use_case)

    asyncio.run(authorization_handler.start(int(config.authorization_ws_port)))
