import logging
import time
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import Optional
from ..database import get_db
from ..models import Retiro
from ..schemas import RetiroCreate, RetiroResponse

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/retiros", response_model=RetiroResponse, status_code=201)
def crear_retiro(retiro: RetiroCreate, db: Session = Depends(get_db)):
    """
    Endpoint para registrar un retiro de inventario.
    ASR: Debe completar en menos de 5 segundos.
    """
    start_time = time.time()
    
    db_retiro = Retiro(
        producto=retiro.producto,
        cantidad=retiro.cantidad,
        operario=retiro.operario
    )
    
    db.add(db_retiro)
    db.commit()
    db.refresh(db_retiro)
    
    elapsed = time.time() - start_time
    logger.info(f"Retiro creado en {elapsed:.3f}s - ID: {db_retiro.id}")
    
    return db_retiro

@router.get("/sql-test")
def sql_injection_test(producto: Optional[str] = Query(None)):
    """
    Endpoint para demostrar resistencia a SQL injection.
    El ORM de SQLAlchemy previene inyecciones automáticamente.
    """
    db = SessionLocal()
    
    try:
        # Intento de consulta con input potencialmente malicioso
        # SQLAlchemy usa prepared statements automáticamente
        
        if producto:
            # Esta consulta está protegida por el ORM
            retiros = db.query(Retiro).filter(Retiro.producto.contains(producto)).limit(10).all()
            count = len(retiros)
        else:
            count = db.query(Retiro).count()
        
        return {
            "message": "Consulta segura ejecutada",
            "input_received": producto,
            "results_count": count,
            "protection": "SQLAlchemy ORM usa prepared statements automáticamente",
            "note": "Las consultas parametrizadas previenen SQL injection al 100%"
        }
        
    except Exception as e:
        logger.error(f"Error en consulta: {str(e)}")
        raise HTTPException(
            status_code=400,
            detail={
                "message": "Error controlado",
                "error": str(e),
                "protection": "Exception handling captura intentos maliciosos"
            }
        )
    finally:
        db.close()

from ..database import SessionLocal