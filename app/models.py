from sqlalchemy import ForeignKey, text, Text
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.database import Base, str_uniq, int_pk, str_null_true
from datetime import date


class User(Base):
    id: Mapped[int_pk]
    email: Mapped[str_uniq]
    hashed_password: Mapped[str]
    admin: Mapped[bool]

    major_id: Mapped[int] = mapped_column(ForeignKey("majors.id"), nullable=False)

    major: Mapped["Major"] = relationship("Major", back_populates="users")

    def __str__(self):
        return (f"{self.__class__.__name__}(id={self.id}, "
                f"first_name={self.first_name!r},"
                f"last_name={self.last_name!r})")

    def __repr__(self):
        return str(self)


class Account(Base):
    id: Mapped[int_pk]
    balance: Mapped[str_uniq]
    major_description: Mapped[str_null_true]
    count_students: Mapped[int] = mapped_column(server_default=text('0'))

    def __str__(self):
        return f"{self.__class__.__name__}(id={self.id}, major_name={self.major_name!r})"

    def __repr__(self):
        return str(self)

# class User(Base):
#     __tablename__ = "users"
#
#     id = Column(Integer, primary_key=True)
#     email = Column(String, unique=True)
#     hashed_password = Column(String)
#     admin = Column(Boolean, default=False)
#
#     accounts = relationship("Account", back_populates="users")
#
#
# class Account(Base):
#     __tablename__ = "accounts"
#
#     id = Column(Integer, primary_key=True)
#     balance = Column(Numeric(18, 2))
#     user_id = Column(Integer, ForeignKey("users.id"))
#
#     users = relationship("User", back_populates="accounts")
#     payments = relationship("Pay", back_populates="accounts")


# class Pay(Base):
#     __tablename__ = "payments"
#
#     transaction_id = Column(String, primary_key=True)
#     amount = Column(Numeric(18, 2))
#     signature = Column(String)
#     account_id = Column(Integer, ForeignKey("accounts.id"))
#
#     accounts = relationship("Account", back_populates="payments")
