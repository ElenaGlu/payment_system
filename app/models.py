from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Numeric
from sqlalchemy.orm import relationship

from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True)
    hashed_password = Column(String)
    admin = Column(Boolean, default=False)

    accounts = relationship("Account", back_populates="users")


class Account(Base):
    __tablename__ = "accounts"

    id = Column(Integer, primary_key=True)
    balance = Column(Numeric(18, 2))
    user_id = Column(Integer, ForeignKey("users.id"))

    users = relationship("User", back_populates="accounts")
    payments = relationship("Pay", back_populates="accounts")


class Pay(Base):
    __tablename__ = "payments"

    transaction_id = Column(String, primary_key=True)
    amount = Column(Numeric(18, 2))
    signature = Column(String)
    account_id = Column(Integer, ForeignKey("accounts.id"))

    accounts = relationship("Account", back_populates="payments")
