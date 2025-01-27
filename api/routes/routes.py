from fastapi import APIRouter
from api.type.type_routes import router as type_routes
from api.montant.montant_routes import router as montant_routes
routers = APIRouter()

routers.include_router(type_routes, prefix="/types", tags=["Type"])
routers.include_router(montant_routes, prefix="/montant", tags=["Montant"])

