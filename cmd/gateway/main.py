from fastapi import FastAPI
import uvicorn

from internal.config import load_config
from internal.app.gateway.usecase import GatewayUseCase
from internal.app.gateway.handler import GatewayHandler

app = FastAPI()

if __name__ == '__main__':
    config = load_config()
    use_case = GatewayUseCase(config.AUTHORIZATION_PORT)
    handler = GatewayHandler(use_case)

    app.include_router(handler.router)
    uvicorn.run(app, port=int(config.GATEWAY_PORT), host="0.0.0.0")