from datetime import datetime
from pydantic import BaseModel
from model.tables import *


class ClosedCredit(BaseModel):
    issuance_date: str = None
    is_closed: bool = None
    return_date: str = None
    body: int = None
    percent: float = None
    total_payments: float = None


class ActualCredit(BaseModel):
    issuance_date: str = None
    is_closed: bool = None
    overdue_days: int = None
    body: float = None
    percent: float = None
    body_payments: float = None
    percent_payments: float = None


def get_credit_info(user_id: int, db):
    credits = db.query(Credit).filter(Credit.user_id == user_id).all()
    credits_list = []
    for credit in credits:
        if credit.actual_return_date != "":
            credit_item = ClosedCredit()
            payments = db.query(Payment).filter(Payment.credit_id == credit.id).all()
            total_payments = round(sum([payment.sum for payment in payments]), 2)

            credit_item.issuance_date = credit.issuance_date
            credit_item.is_closed = True
            credit_item.return_date = credit.return_date
            credit_item.body = credit.body
            credit_item.percent = credit.percent
            credit_item.total_payments = total_payments

            credits_list.append(credit_item)
        else:
            credit_item = ActualCredit()
            body_payments = db.query(Payment).filter(Payment.credit_id == credit.id).filter(Payment.type_id == 1).all()
            total_body_payments = round(sum([payment.sum for payment in body_payments]), 2)
            percent_payments = db.query(Payment).filter(Payment.credit_id == credit.id).filter(Payment.type_id == 2).all()
            total_percent_payments = round(sum([payment.sum for payment in percent_payments]), 2)

            overdue_date = (datetime.now() - datetime.strptime(credit.return_date, '%d.%m.%Y')).days

            credit_item.issuance_date = credit.issuance_date
            credit_item.is_closed = False
            credit_item.overdue_days = overdue_date
            credit_item.body = credit.body
            credit_item.percent = credit.percent
            credit_item.body_payments = total_body_payments
            credit_item.percent_payments = total_percent_payments

            credits_list.append(credit_item)
    return credits_list
