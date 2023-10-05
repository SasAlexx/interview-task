from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from services import credits as CreditsService
router = APIRouter()


@router.get('/{user_id}', tags=['credits'])
async def get_credit_info(user_id: int = None, db: Session = Depends(get_db)):
    return CreditsService.get_credit_info(user_id, db)


