from fastapi import FastAPI

from app.apps.cities.views import router as cities_router


app = FastAPI(title="KaraBUS API", docs_url="/")
app.include_router(cities_router)
