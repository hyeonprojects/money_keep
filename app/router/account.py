from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.schemas.accounts import CreateAccount, LoginAccount, Token, OutputToken, InputRefreshToken
from services.account import create_account, authenticate_account, logout_account
from services.token import create_tokens, get_access_token_account, check_refresh_token, create_access_token

router = APIRouter(
    prefix="/account",
    tags=["account"],
    responses={404: {"description": "Not found"}}
)


@router.post("/register", status_code=201)
async def register(regsiter_account: CreateAccount, db: Session = Depends(get_db)):
    """
    회원가입 기능, 이메일과 비밀번호를 입력하면 계정을 생성함.
    :param regsiter_account: email과 password 값
    :return: 계정 생성 완료 메세지
    """
    try:
        db_account = create_account(db, regsiter_account)
    except SQLAlchemyError:
        raise HTTPException(status_code=status.HTTP_4ti01_UNAUTHORIZED, detail="계정이 생성되지 않았습니다.")
    return {"detail": "계정이 생성 되었습니다."}


@router.post("/login", status_code=200,response_model=OutputToken)
def login(login_account: LoginAccount, db: Session = Depends(get_db)):
    """
    로그인 기능, 이메일과 비밀번호 입력시 검증하고,
    :param login_account: email과 password 값
    :return: access_token값과 refresh_token 값
    """
    try:
        db_account = authenticate_account(db, login_account)
        tokens = create_tokens(db, db_account.account_id)
        output_token = OutputToken(**tokens)
    except SQLAlchemyError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="로그인 도중 문제가 발생했습니다.")
    return output_token


@router.post("/refresh", status_code=200)
async def refresh_token(token: InputRefreshToken, db: Session = Depends(get_db)):
    """
    만료된 access token을 재발급 받기 위해서 refresh token을 받으면 이 값을 비교하여서 access_token을 반환합니다.
    :param token: refresh_token 값
    :return: access_token 값
    """
    try:
        db_account = check_refresh_token(db, token.refresh_token)
        access_token = create_access_token(db_account.account_id)
    except SQLAlchemyError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="토큰 발생 중 문제가 발생했습니다.")
    return {"access_token": "{}".format(access_token)}


@router.get("/logout", status_code=200)
async def logout(account_id: UUID = Depends(get_access_token_account), db: Session = Depends(get_db)):
    """
    access_token 값을 통해서 게정을 찾고 refersh token값을 제거합니다.
    :param account_id: access_token에 있는 계정값
    :return: 로그아웃 종료 알림
    """
    try:
        db_account = logout_account(db, account_id)
    except SQLAlchemyError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="로그아웃 도중 문제가 발생했습니다.")
    return {"detail": "로그아웃 완료"}
