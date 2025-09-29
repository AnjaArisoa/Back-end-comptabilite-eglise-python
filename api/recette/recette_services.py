from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import Session, select, and_, func
from datetime import date, datetime
from typing import List, Optional
from pydantic import BaseModel

from models.eglise_models import Recette
def get_solde_anterieur(db: Session, date_operation: date) -> float:
    """Récupère le solde de la dernière opération avant la date donnée"""
    stmt = (
        select(Recette)
        .where(Recette.date < date_operation)
        .order_by(Recette.date.desc(), Recette.idRecette.desc())
        .limit(1)
    )
    derniere_recette = db.exec(stmt).first()
    return derniere_recette.solde if derniere_recette else 0

def recalculer_soldes_apres_date(db: Session, date_debut: date):
    """Recalcule tous les soldes après une date donnée"""
    stmt = (
        select(Recette)
        .where(Recette.date >= date_debut)
        .order_by(Recette.date, Recette.idRecette)
    )
    recettes = db.exec(stmt).all()
    
    if not recettes:
        return
    
    # Obtenir le solde avant la première recette
    solde_actuel = get_solde_anterieur(db, recettes[0].date)
    
    for recette in recettes:
        # Si c'est le même jour, on part du solde précédent
        if recette.date > date_debut or recette == recettes[0]:
            solde_actuel = solde_actuel - recette.debit_montant + recette.credit_montant
        else:
            solde_actuel = solde_actuel - recette.debit_montant + recette.credit_montant
        
        recette.solde = solde_actuel
        db.add(recette)
    
    db.commit()