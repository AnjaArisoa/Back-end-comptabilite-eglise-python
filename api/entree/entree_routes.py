from fastapi import APIRouter, Depends,status,HTTPException
from sqlalchemy.orm import Session
from fastapi import HTTPException
from api.entree.entree_services import create_entree,get_entree
from api.entree.entree_model import entree_create


from core.database import get_session

router = APIRouter()

@router.post("/create_entree/")
def entree_create(create_data:entree_create,session : Session=Depends(get_session)):
    try:
        return create_entree(create_data,session)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=str(e))
    

@router.get("/get_entree/")
def get_entrees(session : Session=Depends(get_session)):
    try:
        return get_entree(session)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=str(e))