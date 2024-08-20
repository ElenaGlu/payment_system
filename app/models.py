from sqlalchemy import ForeignKey, Numeric, String
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.database import Base, str_uniq, int_pk
from decimal import Decimal


class User(Base):
    id: Mapped[int_pk]
    email: Mapped[str_uniq] = mapped_column(String(120))
    hashed_password: Mapped[str] = mapped_column(String(240))
    admin: Mapped[bool]

    accounts_owner: Mapped["Account"] = relationship(back_populates="owner")


class Pay(Base):
    transaction_id: Mapped[int_pk]
    account_id: Mapped[int_pk] = mapped_column(ForeignKey("accounts.id"))
    amount: Mapped[Decimal] = mapped_column(Numeric(18, 2))
    signature: Mapped[str]

    accounts_payments: Mapped["Account"] = relationship(back_populates="payments")


class Account(Base):
    id: Mapped[int_pk]
    user_id: Mapped[int_pk] = mapped_column(ForeignKey("users.id"))
    balance: Mapped[Decimal] = mapped_column(Numeric(18, 2))

    owner: Mapped[User] = relationship(back_populates="accounts")
    payments: Mapped[Pay] = relationship(back_populates="accounts")



