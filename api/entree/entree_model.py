from pydantic import BaseModel
from datetime import date, datetime
from typing import Optional

class entree_create(BaseModel):
    date:date
    montant:Optional[float]=0

