from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from models.money_keep import BalanceCategory, Category


class TimeStamp(BaseModel):
    created_at: datetime
    updated_at: datetime


class FinancialLedgeBase(BaseModel):
    memo: str
    income: int = 0
    spending: int = 0
    balance_category: BalanceCategory
    category: Category
    short_url: str | None = None


class FinancialLedge(FinancialLedgeBase, TimeStamp):
    financial_ledge_id: UUID
    account_id: UUID

    class Config:
        orm_mode = True


class OutputFinancialLedges(BaseModel):
    balance: int = 0
    data: list[FinancialLedge]


class CreateFinancialLedge(FinancialLedgeBase):
    pass


class UpdateFinancialLedge(FinancialLedgeBase):
    pass


class DeleteFinancialLedge(BaseModel):
    financial_ledge_id: UUID
