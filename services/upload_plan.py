from io import BytesIO
from fastapi import UploadFile, HTTPException
from pydantic import BaseModel
import pandas as pd
from model.tables import *
from sqlalchemy.orm import Session


class CorrectPlan(BaseModel):
    preiod: str = None,
    sum: int = None,
    category_id: int = None


def upload_plan(file: UploadFile, db: Session):

    data = file.file.read()
    obj = pd.read_excel(BytesIO(data)).to_records()
    print(obj)
    categories = {"видача": 3, "збір": 4}

    for x in obj:
        date_obj = pd.to_datetime(x[1]).date()
        plan_date = date_obj.strftime("%d.%m.%Y")
        if plan_date.split('.')[0] != '01':
            raise HTTPException(status_code=404, detail="Date must start with 01!")
        print(plan_date.split('.')[0])
        try:
            plan_sum = int(x[3])
        except:
            raise HTTPException(status_code=404, detail="Wrong format of sum!! Sum can't be empty!")
        plan_category = categories[x[2].lower()]

        existing_plans = db.query(Plan.period).filter(plan_category == Plan.category_id).all()
        existing_plans = [plan[0] for plan in existing_plans]

        if plan_date in existing_plans:
            raise HTTPException(status_code=404, detail="Same plan already exists!")

        print(plan_date, plan_sum, plan_category)

        plan = Plan(
            period=plan_date,
            sum=plan_sum,
            category_id=plan_category)

        try:
            db.add(plan)
            db.commit()
            db.refresh(plan)

        except Exception as e:
            print(e)

    return {"message": "The plans have been successfully entered into the database!"}