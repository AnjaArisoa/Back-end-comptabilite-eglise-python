from fastapi import APIRouter, Depends,status,HTTPException
from sqlalchemy.orm import Session
from fastapi import HTTPException
from api.entree.entree_services import create_entree,get_entree,get_balance_per_month,search_entree_or_sortie,get_details_for_month_and_year
from api.entree.entree_model import entree_create
from datetime import date, datetime


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
    
@router.get("/get_balance_per_months/")
def get_balance_per_months(start_time: date = None, end_time: date = None, session: Session=Depends(get_session),page: int = 1, number_items: int = 50):
    try:
        return get_balance_per_month(start_time,end_time,session,page,number_items)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=str(e))
    
@router.get("/search_entree_or_sortie/")
def search_entree_or_sorties(label:str,start_time: date = None, end_time: date = None,session: Session=Depends(get_session),page: int = 1, number_items: int = 50):
    try:
        return search_entree_or_sortie(label,start_time,end_time,session,page,number_items)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=str(e))
    
@router.get("/get_details_for_month_and_year/")
def get_details_for_month_and_years(month: int, year: int,session: Session=Depends(get_session)):
    try:
        return get_details_for_month_and_year(month,year,session)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=str(e))