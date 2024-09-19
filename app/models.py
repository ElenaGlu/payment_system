from sqlalchemy import ForeignKey, Numeric, String
from sqlalchemy.orm import relationship, Mapped, mapped_column
from decimal import Decimal

from app.database import Base


class User(Base):
    __tablename__ = "user_account"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    full_name: Mapped[str] = mapped_column(String(250))
    hashed_password: Mapped[str] = mapped_column(String())
    admin: Mapped[bool] = mapped_column(default=False)

    wallets: Mapped["Wallet"] = relationship(back_populates="user", cascade="all, delete-orphan")


class Wallet(Base):
    __tablename__ = "user_wallet"

    id: Mapped[int] = mapped_column(primary_key=True)
    name_wallet: Mapped[str] = mapped_column(String(50))
    balance: Mapped[Decimal] = mapped_column(Numeric(18, 2))
    user_id: Mapped[int] = mapped_column(ForeignKey("user_account.id"))

    user: Mapped["User"] = relationship(back_populates="wallets")

