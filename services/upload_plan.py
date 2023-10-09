from io import BytesIO
from fastapi import UploadFile, HTTPException
import pandas as pd
from model.tables import *
from sqlalchemy.orm import Session


def upload_plan(file: UploadFile, db: Session):

    data = file.file.read()
    obj = pd.read_excel(BytesIO(data)).to_records()
    plans = []
    exception = HTTPException(status_code=404, detail="You have an error in your excel file!!")
    try:
        for x in obj:
            date_obj = pd.to_datetime(x[1]).date()
            plan_date = date_obj.strftime("%d.%m.%Y")
            if plan_date.split('.')[0] != '01':
                exception = HTTPException(status_code=404, detail="Date must start with 01!")
                raise exception
            try:
                plan_sum = int(x[3])
            except:
                exception = HTTPException(status_code=404, detail="Wrong format of sum!! Sum can't be empty!")
                raise exception
            plan_category = db.query(Dictionary.id).filter(Dictionary.name == x[2].lower()).scalar()

            existing_plans = db.query(Plan).filter(plan_category == Plan.category_id).all()
            existing_plans = [plan.period for plan in existing_plans]
            if date_obj in existing_plans:
                exception = HTTPException(status_code=404, detail="Same plan already exists!")
                raise exception

            plan = Plan(
                period=date_obj,
                sum=plan_sum,
                category_id=plan_category)
            plans.append(plan)
    except Exception:
        raise exception

    try:
        for plan in plans:
            db.add(plan)
            db.commit()
            db.refresh(plan)

    except Exception as e:
        print(e)

    return {"message": "The plans have been successfully entered into the database!"}