from pydantic import BaseModel, ValidationError
from model.tables import *
from sqlalchemy.orm import Session
from sqlalchemy import extract


class PlanInfo(BaseModel):
    month_year: str
    credits_month_count: int
    credits_month_plan_sum: float
    credits_month_actual_sum: float
    credits_implementation_percent: float
    payments_month_count: int
    payments_month_plan_sum: float
    payments_month_actual_sum: float
    payments_implementation_percent: float
    total_credits_percent: float
    total_payments_percent: float


def year_perfomance(year: int, db: Session):
    year_plans = db.query(Plan).filter(extract('year', Plan.period) == year).all()
    months = sorted(list(set(month.period for month in year_plans)))

    year_credits_sum = db.query(Credit.body).filter(extract('year', Credit.issuance_date) == year).all()
    year_payments_sum = db.query(Payment.sum).filter(extract('year', Payment.payment_date) == year).all()
    year_credits_sum = sum([credit[0] for credit in year_credits_sum])
    year_payments_sum = round(sum([payment[0] for payment in year_payments_sum]))

    all_year_plans = []

    for month in months:
        credits_plans = db.query(Plan).filter(Plan.period == month).filter(Plan.category_id == 3).all()
        payments_plans = db.query(Plan).filter(Plan.period == month).filter(Plan.category_id == 4).all()
        plan_info = {}
        plan_info['month_year'] = f'{month.month}.{month.year}'

        for plan in credits_plans:
            if plan.category_id == 3:
                plan_info['credits_month_plan_sum'] = db.query(Plan.sum).filter(Plan.period == month).filter(
                    Plan.category_id == 3).scalar()

                plan_credits = db.query(Credit).filter(extract('year', Credit.issuance_date) == year).filter(
                    extract('month', Credit.issuance_date) == month.month).all()
                credits_sum = [credit.body for credit in [credits for credits in plan_credits]]
                plan_info['credits_month_count'] = len(plan_credits)
                plan_info['credits_month_actual_sum'] = sum(credits_sum)

                plan_info['credits_implementation_percent'] = round(plan_info['credits_month_actual_sum']/
                                                                 plan_info['credits_month_plan_sum'], 2)

                plan_info['total_credits_percent'] = round(plan_info['credits_month_actual_sum']/
                                                        year_credits_sum, 2)
        for plan in payments_plans:
            if plan.category_id == 4:
                plan_info['payments_month_plan_sum'] = db.query(Plan.sum).filter(Plan.period == month).filter(
                    Plan.category_id == 4).scalar()

                plan_payments = db.query(Payment).filter(extract('year', Payment.payment_date) == year).filter(extract('month', Payment.payment_date) == month.month).all()
                payments_sum = [payment.sum for payment in [payments for payments in plan_payments]]
                plan_info['payments_month_count'] = len(plan_payments)
                plan_info['payments_month_actual_sum'] = round(sum(payments_sum))

                plan_info['payments_implementation_percent'] = round(plan_info['payments_month_actual_sum'] /
                                                                  plan_info['payments_month_plan_sum'], 2)
                plan_info['total_payments_percent'] = round(plan_info['payments_month_actual_sum']/
                                                         year_payments_sum, 2)
        try:
            PlanInfo.model_validate(plan_info)
            plan_info = PlanInfo(**plan_info)
            all_year_plans.append(plan_info)
        except ValidationError as e:
            raise e
    return all_year_plans

