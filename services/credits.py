import datetime
from pydantic import BaseModel, ValidationError
from model.tables import *


class ClosedCredit(BaseModel):
    issuance_date: datetime.date
    is_closed: bool
    return_date: datetime.date
    body: int
    percent: float
    total_payments: float


class ActualCredit(BaseModel):
    issuance_date: datetime.date
    is_closed: bool
    overdue_days: int
    body: float
    percent: float
    body_payments: float
    percent_payments: float


def get_credit_info(user_id: int, db):
    credits = db.query(Credit).filter(Credit.user_id == user_id).all()
    credits_list = []
    for credit in credits:
        if isinstance(credit.actual_return_date, datetime.date):
            credit_item = {}
            payments = db.query(Payment).filter(Payment.credit_id == credit.id).all()
            credit_item['total_payments'] = round(sum([payment.sum for payment in payments]), 2)
            credit_item['issuance_date'] = credit.issuance_date

            credit_item['is_closed'] = True
            credit_item['return_date'] = credit.return_date
            credit_item['body'] = credit.body
            credit_item['percent'] = credit.percent

            try:
                ClosedCredit.model_validate(credit_item)
                credit_item = ClosedCredit(**credit_item)
                credits_list.append(credit_item)
            except ValidationError as e:
                raise e


        else:
            credit_item = {}
            body_payments = db.query(Payment).filter(Payment.credit_id == credit.id).filter(Payment.type_id == 1).all()
            total_body_payments = round(sum([payment.sum for payment in body_payments]), 2)
            percent_payments = db.query(Payment).filter(Payment.credit_id == credit.id).filter(Payment.type_id == 2).all()
            total_percent_payments = round(sum([payment.sum for payment in percent_payments]), 2)

            overdue_days = (datetime.datetime.now().date() - credit.return_date)
            credit_item['issuance_date'] = credit.issuance_date
            credit_item['is_closed'] = False
            credit_item['overdue_days'] = overdue_days.days
            credit_item['body'] = credit.body
            credit_item['percent'] = credit.percent
            credit_item['body_payments'] = total_body_payments
            credit_item['percent_payments'] = total_percent_payments

            try:
                ActualCredit.model_validate(credit_item)
                credit_item = ActualCredit(**credit_item)
                credits_list.append(credit_item)
            except ValidationError as e:
                raise e

    return credits_list
