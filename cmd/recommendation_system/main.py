from fastapi import FastAPI
import uvicorn
import pandas as pd

from internal.config import load_config

from internal.app.recommendation_system.repository import RecommendationSystemRepository
from internal.app.recommendation_system.usecase import RecommendationSystemUseCase
from internal.app.recommendation_system.handler import RecommendationSystemHandler
from internal.domain.repository import ProductRepository, ReviewRepository
from internal.infrastructure.postgres import Database
from ml.recommendation_system.model import RecommendationSystem

app = FastAPI()

if __name__ == '__main__':
    config = load_config()

    df = pd.read_csv('ml/recommendation_system/data/ratings.csv', sep=',')
    ml = RecommendationSystem(df).load_data().train_model()

    db = Database(
        f"postgresql://{config.POSTGRES_USER}:{config.POSTGRES_PASSWORD}@postgres:{config.POSTGRES_PORT}/{config.POSTGRES_DB}")

    products = ProductRepository(db)
    reviews = ReviewRepository(db)

    repo = RecommendationSystemRepository(products, reviews)
    use_case = RecommendationSystemUseCase(repo=repo, ml=ml)
    handler = RecommendationSystemHandler(use_case)

    app.include_router(handler.router)
    uvicorn.run(app, port=int(
        config.RECOMMENDATION_SYSTEM_PORT), host="0.0.0.0")
