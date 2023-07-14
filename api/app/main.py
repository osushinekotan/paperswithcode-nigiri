import dotenv
from fastapi import FastAPI

from app.routers import health, paper, summary

dotenv.load_dotenv()


app = FastAPI(docs_url="/docs/swagger")
app.include_router(health.router)
app.include_router(summary.router)
app.include_router(paper.router)
