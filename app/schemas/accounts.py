import datetime

from pydantic import BaseModel

from models.account import AccountStatus


class AccountBase(BaseModel):
    email: str
    password: str


class TimeStamp(BaseModel):
    created_at: datetime.datetime
    updated_at: datetime.datetime


class Account(AccountBase, TimeStamp):
    refresh_token: str | None
    status: AccountStatus = AccountStatus.user

    class Config:
        orm_mode = True


class CreateAccount(AccountBase):
    pass


class LoginAccount(AccountBase):
    pass


class Token(BaseModel):
    access_token: str
    refresh_token: str


class InputRefreshToken(BaseModel):
    refresh_token: str


class OutputToken(Token):
    pass
