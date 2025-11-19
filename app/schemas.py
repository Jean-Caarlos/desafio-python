# app/schemas.py
from datetime import date
from pydantic import BaseModel, Field, ConfigDict


class DocumentBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    titulo: str = Field(..., max_length=255)
    autor: str = Field(..., max_length=255)
    conteudo: str
    data: date


class DocumentCreate(DocumentBase):
    latitude: float
    longitude: float


class DocumentOut(DocumentBase):
    id: int
    latitude: float
    longitude: float
