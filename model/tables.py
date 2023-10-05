from sqlalchemy import Boolean, Column, Integer, String, Date, ForeignKey, Float
from sqlalchemy.orm import relationship

from database import Base


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    login = Column(String)
    registration_date = Column(Date)
    credits = relationship("Credit", back_populates="users", uselist=True)


class Credit(Base):
    __tablename__ = 'credits'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    issuance_date = Column(String)
    return_date = Column(String)
    actual_return_date = Column(String)
    body = Column(Integer)
    percent = Column(Float)
    users = relationship("User", back_populates="credits", uselist=False)


class Dictionary(Base):
    __tablename__ = 'dictionary'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    plans = relationship("Plan", back_populates="category", uselist=True)
    payments = relationship("Payment", back_populates="category", uselist=True)


class Plan(Base):
    __tablename__ = 'plans'

    id = Column(Integer, primary_key=True, autoincrement=True)
    period = Column(String)
    sum = Column(Integer)
    category_id = Column(Integer, ForeignKey('dictionary.id'))

    category = relationship("Dictionary", back_populates="plans", uselist=True)


class Payment(Base):
    __tablename__ = 'payments'

    id = Column(Integer, primary_key=True, autoincrement=True)
    credit_id = Column(Integer, ForeignKey('credits.id'))
    payment_date = Column(String)
    type_id = Column(Integer, ForeignKey('dictionary.id'))
    sum = Column(Float)

    category = relationship("Dictionary", back_populates="payments", uselist=True)




