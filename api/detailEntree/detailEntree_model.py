from pydantic import BaseModel
from datetime import date, datetime
from typing import Optional

class detailEntree_create(BaseModel):
    montant:float
    quantite:Optional[int]=0
    total:Optional[float]=0
    entree_id:str
    type_id:int

