from sqlalchemy import String, Text, JSON, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.base import Base

class Client(Base):
    __tablename__ = "clients"

    client_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100))
    age: Mapped[int] = mapped_column()
    annual_income: Mapped[float] = mapped_column()
    risk_profile: Mapped[str] = mapped_column(String(50))
    investment_goals: Mapped[list] = mapped_column(JSON)
    time_horizon: Mapped[str] = mapped_column(String(50))
    current_savings: Mapped[float] = mapped_column()
    monthly_surplus: Mapped[float] = mapped_column()
    dependents: Mapped[int] = mapped_column()
    employment_status: Mapped[str] = mapped_column(String(50))
    investment_experience: Mapped[str] = mapped_column(String(50))

    analyse_history: Mapped[list["AnalyseHistory"]] = relationship(back_populates="client")

class Product(Base):
    __tablename__ = "products"

    product_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100))
    risk_level: Mapped[str] = mapped_column(String(50))
    description: Mapped[str] = mapped_column(Text)

class AnalyseHistory(Base):
    __tablename__ = "analyse_history"

    analysis_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    client_id: Mapped[int] = mapped_column(ForeignKey("clients.client_id"), nullable=False)
    analysis_result: Mapped[dict] = mapped_column(JSON)

    client: Mapped["Client"] = relationship(back_populates="analyse_history")
