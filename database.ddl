# DB 생성
CREATE DATABASE money_keep;

# Dev user
CREATE USER 'dev'@'%' identified by 'dev';
GRANT ALL PRIVILEGES on money_keep.* to 'dev'@'%';

# Autocommit 확인
SELECT @@AUTOCOMMIT;
SET AUTOCOMMIT=FALSE;

# 테이블은 SQLAlchemy로 작성되어서 개발 완료 되었습니다.
