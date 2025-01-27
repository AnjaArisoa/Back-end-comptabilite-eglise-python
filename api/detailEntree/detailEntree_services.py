
from sqlmodel import Session, select
from fastapi import HTTPException
from datetime import timedelta
from sqlmodel import Session, select,func,extract
from api.detailEntree.detailEntree_model import detailEntree_create
from models.eglise_models import DetailEntree
import logging
logging.basicConfig(level=logging.INFO)

def create_detailEntree(detail: detailEntree_create, session : Session):
    try:
        charge : DetailEntree = DetailEntree(entree_id=detail.entree_id,type_id=detail.type_id,montant=detail.montant,quantite=detail.quantite,total=detail.total)
        session.add(charge)
        session.commit()
        session.refresh(charge)
        return "insertion réussie"
    except Exception as e:
        return {"messageError": f"Error: {str(e)}"}


def get_detailEntree(session:Session):
    try:
        type = session.exec(select(DetailEntree)).all()
        return type
    except Exception as e:
        return {"messageError":f"{str(e)}"}
    
    


    