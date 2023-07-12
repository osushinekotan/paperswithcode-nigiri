from fastapi import FastAPI

from paperswithcode_nigiri.routers import health

app = FastAPI()
app.include_router(health.router)
