from pydantic import BaseModel
from model.tables import *
from sqlalchemy.orm import Session


class PlanInfo(BaseModel):
    month_year: str = None
    credits_month_count: int = 0
    credits_month_plan_sum: float = 0
    credits_month_actual_sum: float = 0
    credits_implementation_percent: float = 0.0
    payments_month_count: int = 0
    payments_month_plan_sum: float = 0
    payments_month_actual_sum: float = 0
    payments_implementation_percent: float = 0.0
    total_credits_percent: float = 0.0
    total_payments_percent: float = 0.0


def year_perfomance(year: str, db: Session):
    year_plans = db.query(Plan).filter(Plan.period.ilike(f'%{year}')).all()
    months = sorted(list(set(month.period for month in year_plans)))

    year_credits_sum = db.query(Credit.body).filter(Credit.issuance_date.ilike(f'%{year}')).all()
    year_payments_sum = db.query(Payment.sum).filter(Payment.payment_date.ilike(f'%{year}')).all()
    year_credits_sum = sum([credit[0] for credit in year_credits_sum])
    year_payments_sum = round(sum([payment[0] for payment in year_payments_sum]))

    all_year_plans = []

    for month in months:
        credits_plans = db.query(Plan).filter(Plan.period == month).filter(Plan.category_id == 3).all()
        payments_plans = db.query(Plan).filter(Plan.period == month).filter(Plan.category_id == 4).all()

        plan_info = PlanInfo()

        for plan in credits_plans:
            plan_info.month_year = month[3:]
            if plan.category_id == 3:
                plan_info.credits_month_plan_sum = db.query(Plan.sum).filter(Plan.period == month).filter(
                    Plan.category_id == 3).scalar()

                plan_credits = db.query(Credit).filter(Credit.issuance_date.ilike(f'%{month[3:]}')).all()
                credits_sum = [credit.body for credit in [credits for credits in plan_credits]]
                plan_info.credits_month_count = len(plan_credits)
                plan_info.credits_month_actual_sum = sum(credits_sum)

                plan_info.credits_implementation_percent = round(plan_info.credits_month_actual_sum/
                                                            plan_info.credits_month_plan_sum, 2)

                plan_info.total_credits_percent = round(plan_info.credits_month_actual_sum/
                                                        year_credits_sum, 2)
        for plan in payments_plans:
            plan_info.month_year = month[3:]
            if plan.category_id == 4:
                plan_info.payments_month_plan_sum = db.query(Plan.sum).filter(Plan.period == month).filter(
                    Plan.category_id == 4).scalar()

                plan_payments = db.query(Payment).filter(Payment.payment_date.ilike(f'%{month[3:]}')).all()
                payments_sum = [payment.sum for payment in [payments for payments in plan_payments]]
                plan_info.payments_month_count = len(plan_payments)
                plan_info.payments_month_actual_sum = round(sum(payments_sum))

                plan_info.payments_implementation_percent = round(plan_info.payments_month_actual_sum /
                                                             plan_info.payments_month_plan_sum, 2)
                plan_info.total_payments_percent = round(plan_info.payments_month_actual_sum/
                                                        year_payments_sum, 2)
            all_year_plans.append(plan_info)
    return all_year_plans

