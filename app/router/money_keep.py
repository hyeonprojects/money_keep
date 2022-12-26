from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status, Path
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from dependencies import get_db
from schemas.money_keep import CreateFinancialLedge, OutputFinancialLedges, UpdateFinancialLedge
from services.account import get_account
from services.money_keep import create_financial_ledge, get_financial_ledges, get_financial_ledge, \
    update_financial_ledge, remove_money_keep, copy_money_keep_template
from services.token import get_access_token_account

router = APIRouter(
    tags=["money_keep"],
    responses={404: {"description": "Not found"}}
)


@router.post("/money-keep", status_code=200)
def create_money_keep(money_keep_data: CreateFinancialLedge, account_id: UUID = Depends(get_access_token_account), db: Session = Depends(get_db)):
    try:
        db_account = get_account(db, account_id)
        if db_account is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

        db_financial_ledge = create_financial_ledge(db, money_keep_data, account_id)
    except SQLAlchemyError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
    return db_financial_ledge


@router.get("/money-keep", status_code=200, response_model=OutputFinancialLedges)
def read_money_keeps(account_id: UUID = Depends(get_access_token_account), db: Session = Depends(get_db)):
    try:
        db_account = get_account(db, account_id)
        if db_account is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

        db_financial_ledge = get_financial_ledges(db, account_id)
    except SQLAlchemyError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
    return db_financial_ledge


@router.get("/money-keep/{financial_ledge_id}", status_code=200)
def read_money_keep(financial_ledge_id: UUID, account_id: UUID = Depends(get_access_token_account), db: Session = Depends(get_db)):
    try:
        db_account = get_account(db, account_id)
        if db_account is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

        db_financial_ledge = get_financial_ledge(db, financial_ledge_id, account_id)
    except SQLAlchemyError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
    return db_financial_ledge


@router.put("/money-keep/{financial_ledge_id}")
def update_money_keep(money_keep_data: UpdateFinancialLedge, financial_ledge_id: UUID, account_id: UUID = Depends(get_access_token_account), db: Session = Depends(get_db)):
    try:
        db_account = get_account(db, account_id)
        if db_account is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
        db_financial_ledge = update_financial_ledge(db, financial_ledge_id, money_keep_data, account_id)
    except SQLAlchemyError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
    return db_financial_ledge


@router.delete("/money-keep/{financial_ledge_id}")
def delete_money_keep(financial_ledge_id: UUID, account_id: UUID = Depends(get_access_token_account), db: Session = Depends(get_db)):
    try:
        db_account = get_account(db, account_id)
        if db_account is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
        db_financial_ledge_data = remove_money_keep(db, financial_ledge_id)
    except SQLAlchemyError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
    return {"detail": "가계부 기록이 삭제되었습니다."}


@router.post("/money-keep/copy/{financial_ledge_id}")
def copy_money_keep(financial_ledge_id: UUID, account_id: UUID = Depends(get_access_token_account), db: Session = Depends(get_db)):
    try:
        db_account = get_account(db, account_id)
        if db_account is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
        db_copy_financial_ledge = remove_money_keep(db, financial_ledge_id)
    except SQLAlchemyError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
    return db_copy_financial_ledge


@router.post("/money-keep/shorturl")
def short_url():
    pass
