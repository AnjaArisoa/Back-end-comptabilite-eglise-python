
from sqlmodel import Session, select
from fastapi import HTTPException
from datetime import timedelta
from sqlmodel import Session, select,func,extract
from api.entree.entree_model import entree_create
from api.sortie.sortie_services import get_detail_sortie_by_date

from models.eglise_models import Entree,generate_custom_id_entree,DetailEntree,Sortie
import logging
from models.Pagination import Pagination
from datetime import date, datetime
logging.basicConfig(level=logging.INFO)

def create_entree(entree: entree_create, session : Session):
    try:
        new_id=generate_custom_id_entree(session=session)
        charge : Entree = Entree(idEntree=new_id,date=entree.date,montant=0)
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
def update_cp(id_entree:str,montant:float,session : Session):
    
    entree=session.exec(select(Entree).where(Entree.idEntree == id_entree)).first()
    if entree is None:
        raise Exception(f"CP  with id {id_entree} does not exist.")
    
    entree.montant=montant
    session.add(entree)
    session.commit()
    session.refresh(entree)
    return "Modification réussie"

def get_sum_identree(id_entree:str,session:Session):
    try:
        montants = session.exec(
            select(DetailEntree).where(Entree.idEntree== id_entree)
        ).all()
        total_value = sum(montant.valeur for montant in montants)  
        return total_value 
    except Exception as e:
        return {"messageError": f" {str(e)}"}
    

def get_last_id(session:Session):
    statement = select(Entree.idEntree).order_by(Entree.idEntree.desc()).limit(1)
    result = session.exec(statement).first() 
    last_id = result
    return last_id

def get_sum_montant_entree(start_time: date = None, end_time: date = None, session: Session = None):
    query = select(
        extract('month', Entree.date).label("monthEntree"),
        extract('year', Entree.date).label("yearEntree"),
        func.sum(Entree.montant).label("montantEntree"),
        Entree.idEntree.label("idEntree"),
    ).group_by("monthEntree", "yearEntree").order_by("yearEntree", "monthEntree")
    if start_time:
        query = query.where(Entree.date >= start_time)
    if end_time:
        query = query.where(Entree.date <= end_time)

    result = session.exec(query).all()
    return result

def search_entree_or_sortie(label: str, start_time: date = None, end_time: date = None, session: Session = None, page: int = 1, number_items: int = 50):
    try:
        pagination = Pagination(page=page, limit=number_items)
        query = None
        count = None
        if label is not None:
            if label and label.upper() == "STR":
                query = select(
                    Sortie.date.label("dateSortie"),
                    Sortie.idSortie.label("idSortie"),
                    Sortie.montant.label("montantSortie"),
                    Sortie.raison.label("raison")
                )
                count = select(func.count(Sortie.idSortie))
                if start_time is not None and end_time is not None:
                    query = query.where(Sortie.date.between(start_time, end_time))
                    count = count.where(Sortie.date.between(start_time, end_time))
                elif start_time is not None:
                    query = query.where(Sortie.date == start_time)
                    count = count.where(Sortie.date == start_time)
                elif end_time is not None:
                    query = query.where(Sortie.date == end_time)
                    count = count.where(Sortie.date == end_time)
            elif label and label.upper() == 'ETR':
                query = select(
                    Entree.date.label("dateEntree"),
                    Entree.idEntree.label("idEntree"),
                    Entree.montant.label("montantEntree")
                )
                count = select(func.count(Entree.idEntree))
                if start_time is not None and end_time is not None:
                    query = query.where(Entree.date.between(start_time, end_time))
                    count = count.where(Entree.date.between(start_time, end_time))
                elif start_time is not None:
                    query = query.where(Entree.date == start_time)
                    count = count.where(Entree.date == start_time)
                elif end_time is not None:
                    query = query.where(Entree.date == end_time)
                    count = count.where(Entree.date == end_time)

            query = query.offset(pagination.offset).limit(pagination.limit)  # Appliquer la pagination
            result = session.exec(query).all()
            c = session.exec(count).first()

            # Formatter le résultat en liste de dictionnaires
            formatted_result = [
                {
                    "dateEntree": row.dateEntree if label.upper() == "ETR" else row.dateSortie,
                    "idEntree": row.idEntree if label.upper() == "ETR" else row.idSortie,
                    "montantEntree": row.montantEntree if label.upper() == "ETR" else row.montantSortie,
                    "raison": row.raison if label.upper() == "STR" else None
                }
                for row in result
            ]

        pagination.total_items = c
        return {"data": formatted_result, "pagination": pagination.dict()}

    except Exception as e:
        return {"messageError": f"Error: {str(e)}"}

def get_balance_per_month(start_time: date = None, end_time: date = None, session: Session = None, page: int = 1, number_items: int = 50):
    try:
        pagination = Pagination(page=page, limit=number_items)
        entree_query = select(
            extract('month', Entree.date).label("month"),
            extract('year', Entree.date).label("year"),
            func.coalesce(func.sum(Entree.montant), 0).label("total_entree")
        ).group_by(extract('year', Entree.date), extract('month', Entree.date)).alias("entrees")
        sortie_query = select(
            extract('month', Sortie.date).label("month"),
            extract('year', Sortie.date).label("year"),
            func.coalesce(func.sum(Sortie.montant), 0).label("total_sortie")
        ).group_by(extract('year', Sortie.date), extract('month', Sortie.date)).alias("sorties")
        query = select(
            entree_query.c.month,
            entree_query.c.year,
            entree_query.c.total_entree,
            sortie_query.c.total_sortie,
            (entree_query.c.total_entree - sortie_query.c.total_sortie).label("balance")
        ).outerjoin(
            sortie_query, 
            (entree_query.c.month == sortie_query.c.month) & (entree_query.c.year == sortie_query.c.year)
        ).order_by(entree_query.c.year, entree_query.c.month)
        if start_time:
            query = query.where(entree_query.c.year >= start_time.year, entree_query.c.month >= start_time.month)
        if end_time:
            query = query.where(entree_query.c.year <= end_time.year, entree_query.c.month <= end_time.month)
        count_query = select(func.count().label("total_count")).select_from(entree_query)
        c = session.exec(count_query).first()
        result = session.exec(query).all()
        formatted_result = [
            {
                "month": row.month,
                "year": row.year,
                "total_entree": row.total_entree,
                "total_sortie": row.total_sortie if row.total_sortie is not None else 0,
                "balance": row.balance if row.balance is not None else 0
            }
            for row in result
        ]
        pagination.total_items = c
        return {"data": formatted_result, "pagination": pagination.dict()}

    except Exception as e:
        return {"messageError": f"Error: {str(e)}"}
    


def get_details_for_month_and_year(month: int, year: int, session: Session):
    from api.detailEntree.detailEntree_services import read_detail_entree_by_date
    try:
        entree_details = read_detail_entree_by_date(month, year, session)
        sortie_details = get_detail_sortie_by_date(month, year, session)

        # Agrégation des entrées par jour
        entree_details_by_day = {}
        for entree in entree_details:
            day = entree["day"]
            if day not in entree_details_by_day:
                entree_details_by_day[day] = []
            # Ajouter les détails d'entrée sous la forme d'un dictionnaire
            entree_details_by_day[day].extend(entree["details"])

        # Agrégation des sorties par jour
        sortie_details_by_day = {}
        for sortie in sortie_details:
            day = sortie["dateSortie"].day  # Assurez-vous que la date est sous forme de datetime
            if day not in sortie_details_by_day:
                sortie_details_by_day[day] = []
            sortie_details_by_day[day].append({
                "idSortie": sortie["idSortie"],
                "montantSortie": sortie["montantSortie"],
                "raison": sortie["raison"]
            })

        # Retourner les détails regroupés par jour
        return {
            "month": month,
            "year": year,
            "entree_details": [{"day": day, "details": details} for day, details in entree_details_by_day.items()],
            "sortie_details": [{"day": day, "details": details} for day, details in sortie_details_by_day.items()]
        }

    except Exception as e:
        return {"messageError": str(e)}














        


    
    


    