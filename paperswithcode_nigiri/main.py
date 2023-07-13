import dotenv
from fastapi import FastAPI

from paperswithcode_nigiri.routers import health, paper

dotenv.load_dotenv()


app = FastAPI(docs_url="/docs/swagger")
app.include_router(health.router)
app.include_router(paper.router)
