from sqlmodel import Field, SQLModel, Relationship
from typing import List, Optional
from datetime import date, datetime, timedelta, time
from enum import Enum
from sqlalchemy import Index
from sqlalchemy import PrimaryKeyConstraint, Index, UniqueConstraint
from core.utils import *


class StatusEnum(str, Enum):
    active = "active"
    

def get_current_time_plus_3_hours() -> datetime:
    return datetime.utcnow() + timedelta(hours=3)


class TimestampMixin(SQLModel):
    created_at: datetime = Field(default_factory=get_current_time_plus_3_hours, nullable=False)
    updated_at: datetime = Field(default_factory=get_current_time_plus_3_hours, nullable=False)

class Type(TimestampMixin,table=True):
    idType:Optional[int] = Field(default=None, primary_key=True)
    nom:Optional[str]
    detailEntree:List["DetailEntree"] = Relationship(back_populates="type")
    __table_args__ = (Index("ix_type_id", "idType"),)

class Montant(TimestampMixin,table=True):
    idMontant: Optional[int] = Field(default=None, primary_key=True)
    montant:Optional[float]=0
    __table_args__ = (Index("ix_montant_id", "idMontant"),)

class Sortie(TimestampMixin,table=True):
    idSortie:Optional[str]= Field(default=None, primary_key=True)
    date:date
    montant:Optional[float]
    raison:Optional[str]
    __table_args__ = (Index("ix_sortie_id", "idSortie"),)

class Entree(TimestampMixin,table=True):
    idEntree:Optional[str]=Field(default=None,primary_key=True)
    date:date
    montant:Optional[float]=0
    detailEntree: List["DetailEntree"] = Relationship(back_populates="entree")
    __table_args__ = (Index("ix_entree_id", "idEntree"),)

class DetailEntree(TimestampMixin,table=True):
    idDetailEntree:Optional[str]=Field(default=None,primary_key=True)
    entree_id:Optional[str]=Field(foreign_key="entree.idEntree")
    montant:Optional[float]
    quantite:Optional[int]=0
    total:Optional[float]=0
    type_id: Optional[int] = Field(foreign_key="type.idType")
    type: List["Type"] = Relationship(back_populates="detailEntree")
    entree: List["Entree"] = Relationship(back_populates="detailEntree")
    __table_args__ = (Index("ix_detail_entree_id", "idDetailEntree"),)






