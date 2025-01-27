
from sqlmodel import Session, select
from fastapi import HTTPException
from datetime import timedelta
from sqlmodel import Session, select,func,extract
from api.sortie.sortie_model import sortie_create
from models.eglise_models import Sortie,generate_custom_id_sortie
import logging
logging.basicConfig(level=logging.INFO)

def create_sortie(sortie: sortie_create, session : Session):
    try:
        new_id=generate_custom_id_sortie(session=session)
        sortie : Sortie = Sortie(idSortie=new_id,date=sortie.date_sortie,montant=sortie.montant,raison=sortie.raison)
        session.add(sortie)
        session.commit()
        session.refresh(sortie)
        return "insertion réussie"
    except Exception as e:
        return {"messageError": f"Error: {str(e)}"}


def get_sortie(session:Session):
    try:
        type = session.exec(select(Sortie)).all()
        return type
    except Exception as e:
        return {"messageError":f"{str(e)}"}
    
    


    