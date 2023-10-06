from fastapi import APIRouter, Depends, UploadFile
from sqlalchemy.orm import Session
from database import get_db
from services import upload_plan as PlanService
from services import plans_perfomance as PlansPerfomanceService

router = APIRouter()


@router.post('/plans_insert', tags=['upload_plans'])
async def upload_file(file: UploadFile, db: Session = Depends(get_db)):
    return PlanService.upload_plan(file, db)


@router.get('/plans_perfomance', tags=['plans_perfomance'], description='method expects a date in the form "DD.MM.YYYY"')
async def get_plan_info(date: str, db: Session = Depends(get_db)):
    return PlansPerfomanceService.plans_perfomance(date, db)
