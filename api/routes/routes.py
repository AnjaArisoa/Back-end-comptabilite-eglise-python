from fastapi import APIRouter
from api.type.type_routes import router as type_routes
routers = APIRouter()

routers.include_router(type_routes, prefix="/types", tags=["Type"])

