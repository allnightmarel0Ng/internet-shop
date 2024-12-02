from internal.config import *
from internal.infrastructure.postgres import Database
from internal.domain.repository import UserRepository
from internal.infrastructure.kafka import Consumer, wait_for_topic

from internal.app.money_operations.repository import *
from internal.app.money_operations.usecase import *
from internal.app.money_operations.handler import *


if __name__ == '__main__':
    # try:
    config = load_config()

    db = Database(
        f"postgresql://{config.POSTGRES_USER}:{config.POSTGRES_PASSWORD}@postgres:{config.POSTGRES_PORT}/{config.POSTGRES_DB}")

    user_repository = UserRepository(db)
    repository = MoneyOperationsRepository(user_repository)
    use_case = MoneyOperationsUseCase(repository)


    wait_for_topic(f"kafka:{config.KAFKA_PORT}", 'money_operations')

    consumer = Consumer(f"kafka:{config.KAFKA_PORT}", 'group')
    consumer.subscribe(['money_operations'])
    handler = MoneyOperationsHandler(use_case=use_case, consumer=consumer)


    handler.consume()

    # except Exception as e:
    #     print('error: unable to establish the server: ', str(e))
