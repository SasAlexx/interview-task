from datetime import datetime
from pydantic import BaseModel, ValidationError
from sqlalchemy import extract
from model.tables import *
from sqlalchemy.orm import Session


class PlanInfo(BaseModel):
    month: int
    category: str
    plan_sum: float
    actual_sum: float
    implementation_percent: float


'method expects a date in the form "DD.MM.YYYY"'


def plans_perfomance(date: str, db: Session):
    date_obj = datetime.strptime(date, '%d.%m.%Y').date()
    plans_db = db.query(Plan).filter(extract('year', Plan.period) == date_obj.year).filter(extract('month', Plan.period) == date_obj.month).all()
    payments_db = db.query(Payment).filter(extract('year', Payment.payment_date) == date_obj.year).filter(extract('month', Payment.payment_date) == date_obj.month).all()
    credits_db = db.query(Credit).filter(extract('year', Credit.issuance_date) == date_obj.year).filter(extract('month', Credit.issuance_date) == date_obj.month).all()

    plans_list = []

    for plan in plans_db:
        current_plan = {}
        current_plan['month'] = date_obj.month
        current_plan['category'] = db.query(Dictionary.name).filter(Dictionary.id == plan.category_id).scalar()

        current_plan['plan_sum'] = plan.sum

        if plan.category_id == 3:
            current_plan['actual_sum'] = round(sum([credit.body for credit in credits_db
                                          if int(credit.issuance_date.day) <= int(date_obj.day)]), 2)
            current_plan['implementation_percent'] = round(current_plan['actual_sum']/current_plan['plan_sum'], 2)

        elif plan.category_id == 4:
            current_plan['actual_sum'] = round(sum([payment.sum for payment in payments_db
                                           if int(payment.payment_date.day) <= int(date_obj.day)]), 2)
            current_plan['implementation_percent'] = round(current_plan['actual_sum'] / current_plan['plan_sum'], 2)

        try:
            PlanInfo.model_validate(current_plan)
            current_plan = PlanInfo(**current_plan)
            plans_list.append(current_plan)
        except ValidationError as e:
            raise e

    return plans_list
