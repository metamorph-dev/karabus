from fastapi import FastAPI
from fastapi import Request
from fastapi import status
from starlette.responses import JSONResponse

from app.apps.busses.routers import busses_router
from app.apps.cities.routers import cities_router
from app.exceptions.already_exists import AlreadyExistsException
from app.exceptions.not_found import NotFoundException


app = FastAPI(title="KaraBUS API", docs_url="/")
app.include_router(busses_router)
app.include_router(cities_router)


@app.exception_handler(AlreadyExistsException)
async def handle_already_exists_exception(request: Request, exc: AlreadyExistsException):
    return JSONResponse({"detail": str(exc)}, status.HTTP_400_BAD_REQUEST)


@app.exception_handler(NotFoundException)
async def handle_already_exists_exception(request: Request, exc: NotFoundException):
    return JSONResponse({"detail": str(exc)}, status.HTTP_404_NOT_FOUND)
