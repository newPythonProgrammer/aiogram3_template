from sqlalchemy import String, DateTime, ForeignKey, func, BigInteger
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase, relationship
from typing import Optional
import datetime


class Base(DeclarativeBase):
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), default=func.now())
    updated_at: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), default=func.now(),
                                                          onupdate=func.now())

class User(Base):
    __tablename__ = "users"

    user_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    first_name: Mapped[Optional[str]] = mapped_column(String(100))
    last_name: Mapped[Optional[str]] = mapped_column(String(100))
    utm: Mapped[Optional[str]] = mapped_column(String(100), ForeignKey("utm.utm"))

    payments: Mapped[list["Payment"]] = relationship(back_populates="user")


class Payment(Base):
    __tablename__ = "payments"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.user_id"))
    payment_method: Mapped[str] = mapped_column(String(50))

    user: Mapped["User"] = relationship(back_populates="payments")


class UTM(Base):
    __tablename__ = "utm"

    utm: Mapped[str] = mapped_column(String(100), primary_key=True)