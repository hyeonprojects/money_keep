from datetime import datetime, timedelta
from uuid import UUID

from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy import select, update
from sqlalchemy.orm import Session

from dependencies import get_db
from models.account import Account
from schemas.accounts import Token
from services.secret import get_secret


TOKEN_SECRET_KEY = get_secret("TOKEN_SECRET_KEY")
TOKEN_ALGORITHM = get_secret("TOKEN_ALGORITHM")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def create_tokens(db: Session, account_id: str) -> dict:
    refresh_token_expire = datetime.utcnow() + timedelta(
        days=get_secret("REFRESH_TOKEN_EXPIRE_DAYS")
    )

    refresh_token_data = {"account_id": account_id, "exp": refresh_token_expire}

    access_token = create_access_token(account_id)
    refresh_token = jwt.encode(
        refresh_token_data, TOKEN_SECRET_KEY, algorithm=TOKEN_ALGORITHM
    )

    sql = (
        update(Account)
        .where(Account.account_id == account_id)
        .values(refresh_token=refresh_token)
    )
    db_account = db.execute(sql)
    db.commit()

    return {"access_token": access_token, "refresh_token": refresh_token}


def create_access_token(account_id: UUID) -> str:
    """
    access token 생성
    :param account_id: 계정 id
    :return: access_token
    """
    access_token_expire = datetime.utcnow() + timedelta(
        days=get_secret("ACCESS_TOKEN_EXPIRE_HOURS")
    )
    access_token_data = {"account_id": str(account_id), "exp": access_token_expire}
    access_token = jwt.encode(
        access_token_data, TOKEN_SECRET_KEY, algorithm=TOKEN_ALGORITHM
    )
    return access_token


def get_token_payload(token: str) -> dict:
    """
    토큰의 복호화 뒤에 개발 진행
    :param token:
    :return:
    """
    try:
        payload = jwt.decode(token, TOKEN_SECRET_KEY, algorithms=[TOKEN_ALGORITHM])
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="토큰에 문제가 있습니다."
        )
    return payload


def check_access_token(db: Session, access_token: str) -> bool:
    payload = get_token_payload(access_token)
    account_id: UUID = payload.get("account_id")
    sql = select(Account).where(Account.account_id == account_id)
    db_account = db.scalars(sql).one()

    if db_account.account_id:
        return True
    else:
        return False


def check_refresh_token(db: Session, refresh_token: str) -> Account:
    sql = select(Account).where(Account.refresh_token == refresh_token)
    db_account = db.scalars(sql).one()
    return db_account


def get_access_token_account(access_token: str = Depends(oauth2_scheme)) -> str:
    try:
        payload = jwt.decode(access_token, TOKEN_SECRET_KEY, algorithms=TOKEN_ALGORITHM)
        account_id: UUID = payload.get("account_id")
        if account_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="계정에 문제가 있습니다"
            )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="계정에 문제가 있습니다."
        )
    return str(account_id)
