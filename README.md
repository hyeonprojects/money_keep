# Money Keep

>소비 내역 기록/관리하는 서비스

____

## 기술스택
- python3.10
- fastapi
- uvicorn
- sqlalchemy
- pytest
- httpx
- black
- python-jose
- passlib
- mysql 5.7

## Database 설계

### account

| Name | Data Type | Option | 설명 |
| --- | --- | --- | --- |
| account_id | uuid | pk | 고객 id |
| email | varchar (email) | unique | 고객 이메일 |
| password | varchar |  | 고객 비밀번호 |
| refresh_token | varchar | nullalbe | refrehs_token 값 |
| status | enum  | default = 0 | 유저 상태 |
| created_at | datetime |  | 생성날짜 |
| updated_at | datetime |  | 수정날짜 |

status

- 1 : 일반 사용자 use
- 11: 관리자
- 0 : 회원 탈퇴
- 2 : 회원 일시 정지

### financial_ledge

| Name | Data Type | Option | 설명 |
| --- | --- | --- | --- |
| financial_ledge_id | uuid | pk | 가계부 id |
| account_id | uuid | fk | 고객 id |
| memo | varchar |  | 가계부 메모 |
| income | inteager | default=0 | 수입 |
| spending | inteager | default=0 | 지출 |
| balance_category | Enum |  | 돈 카테고리( 돈, 카드, 기타) |
| category | Enum |  | 사용처 분류(식비, 주거통신, 생활용품, 의복미용, 건강문화, 교육육아, 교통차량, 경조사회비, 세금이자, 용돈기타 |
| short_url | varchar | nullable | url를 통해서 |
| created_at | datetime |  | 생성날짜 |
| updated_at | datetime |  | 수정날짜 |

balance_category

- 0 : 임의 입력
- 1 : 현금
- 2 : 카드
- 3 : 기타

category

- 1 : 식비
- 2 : 주거/통신
- 3 : 생활용품
- 4 : 의복/미용
- 5 : 건강/문화
- 6 : 교육/육아
- 7 : 교통/차량
- 8 : 경조사/회비
- 9 : 용돈/기타

