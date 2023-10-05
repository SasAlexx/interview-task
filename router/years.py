from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from services import year_perfomance as YaerPerfomanceService

router = APIRouter()


@router.get('/year_perfomance', tags=['year_perfomance'])
async def get_year_info(year: str, db: Session = Depends(get_db)):
    return YaerPerfomanceService.year_perfomance(year, db)
