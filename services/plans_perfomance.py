from pydantic import BaseModel
from model.tables import *
from sqlalchemy.orm import Session


class PlanInfo(BaseModel):
    month: str = None
    category: int = None
    plan_sum: float = None
    actual_sum: float = None
    implementation_percent: float = None


def plans_perfomance(period: str, db: Session):
    date_obj = period.split('.')
    plans_db = db.query(Plan).filter(Plan.period.ilike(f'%{date_obj[1]}.{date_obj[2]}')).all()
    payments_db = db.query(Payment).filter(Payment.payment_date.ilike(f'%{date_obj[1]}.{date_obj[2]}')).all()
    credits_db = db.query(Credit).filter(Credit.issuance_date.ilike(f'%{date_obj[1]}.{date_obj[2]}')).all()

    plans_list = []

    for plan in plans_db:
        current_plan = PlanInfo()
        current_plan.month = date_obj[1]
        current_plan.category = plan.category_id
        current_plan.plan_sum = plan.sum

        if plan.category_id == 3:
            current_plan.actual_sum = round(sum([credit.body for credit in credits_db
                                          if int(credit.issuance_date[:2]) <= int(date_obj[0])]), 2)
            current_plan.implementation_percent = round(current_plan.actual_sum/current_plan.plan_sum, 2)

        elif plan.category_id == 4:
            current_plan.actual_sum = round(sum([payment.sum for payment in payments_db
                                           if int(payment.payment_date[:2]) <= int(date_obj[0])]), 2)
            current_plan.implementation_percent = round(current_plan.actual_sum / current_plan.plan_sum, 2)

        plans_list.append(current_plan)

    return plans_list
