
from sqlmodel import Session, select
from fastapi import HTTPException
from datetime import timedelta
from sqlmodel import Session, select,func,extract
from api.entree.entree_model import entree_create
from models.eglise_models import Entree,generate_custom_id_entree
import logging
logging.basicConfig(level=logging.INFO)

def create_entree(entree: entree_create, session : Session):
    try:
        new_id=generate_custom_id_entree(session=session)
        charge : Entree = Entree(idEntree=new_id,date=entree.date,montant=entree.montant)
        session.add(charge)
        session.commit()
        session.refresh(charge)
        return "insertion réussie"
    except Exception as e:
        return {"messageError": f"Error: {str(e)}"}


def get_entree(session:Session):
    try:
        type = session.exec(select(Entree)).all()
        return type
    except Exception as e:
        return {"messageError":f"{str(e)}"}
    
    


    