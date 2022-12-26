import uuid
import enum
from datetime import datetime

from sqlalchemy import Column, String, Enum, DateTime

from config.database import Base


class AccountStatus(enum.Enum):
    withdrawal = 0  # 회원 탈퇴
    user = 1  # 일반 사용자
    pause = 2  # 회원 일시 정지
    admin = 11  # 관리자


class Account(Base):
    __tablename__ = "account"

    account_id = Column(String(36), primary_key=True, default=uuid.uuid4(), comment="계정 id")
    email = Column(String(100), unique=True, comment="계정 이메일")
    password = Column(String(150), comment="계정 비밀번호")
    refresh_token = Column(String(300), nullable=True, comment="유저의 refresh 토큰")
    status = Column(Enum(AccountStatus), default=AccountStatus.user, comment="계정 상태값")
    created_at = Column(DateTime, default=datetime.now(), comment="계정 생성 날짜")
    updated_at = Column(DateTime, default=datetime.now(), onupdate=lambda: datetime.now(),
                        comment="계정 데이터 수정 날짜")

    __table_args__ = {"extend_existing": True}
