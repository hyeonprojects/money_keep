from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy import select, update
from sqlalchemy.orm import Session

from models.money_keep import FinancialLedge
from schemas.money_keep import CreateFinancialLedge, UpdateFinancialLedge, OutputFinancialLedges
from services.account import get_account


def create_financial_ledge(db: Session, money_keep_data: CreateFinancialLedge, account_id: UUID):
    db_financial_ledge = FinancialLedge(
        account_id=account_id,
        memo=money_keep_data.memo,
        income=money_keep_data.income,
        spending=money_keep_data.spending,
        balance_category=money_keep_data.balance_category,
        category=money_keep_data.category
    )
    db.add(db_financial_ledge)
    db.commit()
    db.refresh(db_financial_ledge)
    return db_financial_ledge


def update_financial_ledge(db: Session, financial_ledge_id: UUID, money_keep_data: UpdateFinancialLedge, account_id: UUID):
    sql = update(FinancialLedge).where(FinancialLedge.financial_ledge_id == financial_ledge_id,
                                       FinancialLedge.account_id == account_id).values(
        memo=money_keep_data.memo,
        income=money_keep_data.income,
        speding=money_keep_data.spending,
        balance_category=money_keep_data.balance_category,
        category=money_keep_data.category
    )
    db_financial_ledge = db.execute(sql)
    db.commit()
    return db_financial_ledge


def get_financial_ledge(db: Session, financial_ledge_id: UUID, account_id: UUID):
    sql = select(FinancialLedge).where(FinancialLedge.financial_ledge_id == financial_ledge_id)
    db_financial_ledge_id = db.scalars(sql).one()
    return db_financial_ledge_id


def get_financial_ledges(db: Session, account_id: UUID) -> OutputFinancialLedges:
    # 전체 총액도 나오면 좋겠다.
    sql = select(FinancialLedge).where(FinancialLedge.account_id == account_id)
    db_financial_ledge = db.scalars(sql)

    account_balance = 0
    data = []

    for raw in db_financial_ledge:
        account_balance = account_balance + raw.income + raw.spending
        data.append(raw)

    output_financial_ledges = OutputFinancialLedges(
        balance=account_balance,
        data=data
    )

    return output_financial_ledges


def copy_money_keep_template(db: Session, financial_ledge_id: UUID) -> FinancialLedge:
    sql = select(FinancialLedge).where(FinancialLedge.financial_ledge_id == financial_ledge_id)
    db_financial_ledge = db.scalars(sql).one()

    db_copy_financial_ledge = FinancialLedge(
        account_id=db_financial_ledge.account_id,
        memo=db_financial_ledge.memo,
        balance_category=db_financial_ledge.balance_category,
        category=db_financial_ledge.category,
    )
    db.add(db_copy_financial_ledge)
    db.commit()
    db.refresh(db_copy_financial_ledge)

    return db_copy_financial_ledge


def change_delete_money_keep(db: Session, finalcial_ledge_id: UUID):
    sql = update(FinancialLedge).where(FinancialLedge.financial_ledge_id == finalcial_ledge_id).values(
        is_delete=True
    )
    db_financial_ledge = db.execute(sql)
    db.commit()
    return db_financial_ledge


def create_short_url():
    pass
