from sqlalchemy import ForeignKey, text, Text
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.database import Base, str_uniq, int_pk


class User(Base):
    id: Mapped[int_pk]
    email: Mapped[str_uniq]
    hashed_password: Mapped[str]
    admin: Mapped[bool]

    accounts: Mapped["Account"] = relationship("Account", back_populates="users")


class Account(Base):
    id: Mapped[int_pk]
    balance: Mapped[decimal(18, 2)]
    user_id = Mapped[int] = mapped_column(ForeignKey("users.id"))

    users = Mapped["User"] = relationship("User", back_populates="accounts")
    payments = Mapped["Pay"] = relationship("Pay", back_populates="accounts")


class Pay(Base):
    transaction_id: Mapped[int_pk]
    amount = Mapped[decimal(18, 2)]
    signature: Mapped[str]

    account_id = Mapped[int] = mapped_column(ForeignKey("accounts.id"))

    accounts = Mapped["Account"] = relationship("Account", back_populates="payments")
