from fastapi import APIRouter, Depends,status,HTTPException
from sqlalchemy.orm import Session
from fastapi import HTTPException
from api.detailEntree.detailEntree_model import detailEntree_create
from api.detailEntree.detailEntree_services import create_detailEntree,get_detailEntree


from core.database import get_session

router = APIRouter()

@router.post("/create_detailEntree/")
def detailEntree_create(create_data:detailEntree_create,session : Session=Depends(get_session)):
    try:
        return create_detailEntree(create_data,session)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=str(e))
    
@router.get("/get_detailEntree/")
def get_detailentrees(session : Session=Depends(get_session)):
    try:
        return get_detailEntree(session)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=str(e))
