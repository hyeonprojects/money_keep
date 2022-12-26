from uuid import UUID

from fastapi import HTTPException, status
from passlib.context import CryptContext
from sqlalchemy import select, update
from sqlalchemy.orm import Session

from models.account import Account
from schemas.accounts import CreateAccount, LoginAccount

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def create_account(db: Session, account: CreateAccount):
    account.password = get_password_hash(account.password)
    db_account = Account(
        email=account.email,
        password=account.password
    )
    db.add(db_account)
    db.commit()
    db.refresh(db_account)
    return db_account


def authenticate_account(db: Session, account: LoginAccount):
    sql = select(Account).where(Account.email == account.email)
    db_account = db.scalars(sql).one()

    # password 비교
    if not verify_password(account.password, db_account.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="계정이 없거나 비밀번호가 없습니다.")


    return db_account


def get_account(db: Session, account_id: UUID):
    sql = select(Account).where(Account.account_id == account_id)
    db_account = db.scalars(sql).one()
    return db_account


def get_account_by_email(db: Session, email: str):
    sql = select(Account).where(Account.email == email)
    db_account = db.scalars(sql).one()
    return db_account


def logout_account(db: Session, account_id: UUID):
    # refresh token 삭제
    sql = update(Account).where(Account.account_id == account_id).values(refresh_token="")
    db_account = db.execute(sql)
    db.commit()
    return db_account
