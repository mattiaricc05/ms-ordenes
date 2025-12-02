from pydantic import BaseModel, Field, validator
from datetime import datetime
from typing import Optional

class RetiroCreate(BaseModel):
    producto: str = Field(..., min_length=1, max_length=200)
    cantidad: int = Field(..., gt=0)
    operario: str = Field(..., min_length=1, max_length=100)
    
    @validator('producto', 'operario')
    def no_empty_string(cls, v):
        if not v or not v.strip():
            raise ValueError('El campo no puede estar vacío')
        return v.strip()

class RetiroResponse(BaseModel):
    id: int
    producto: str
    cantidad: int
    operario: str
    timestamp: datetime
    
    class Config:
        from_attributes = True