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

## API 설명
- account/register POST : email과 password를 입력하고 계정을 생성
```shell
curl --location --request POST 'http://127.0.0.1:8000/account/register' \
--header 'Content-Type: application/json' \
--data-raw '{
    "email": "payhere@gmail.com",
    "password": "payhere"
}'
```

- account/login POST : email과 password를 입력하고 access token과 refresh token을 발급받습니다.
```shell
curl --location --request POST 'http://127.0.0.1:8000/account/login' \
--header 'Content-Type: application/json' \
--data-raw '{
    "email": "payhere@gmail.com",
    "password": "payhere"
}'
```

- account/refresh POST : refersh_token을 보내어서 access token을 재발급 받습니다. (예제 토큰입니다.)
```shell
curl --location --request POST 'http://127.0.0.1:8000/account/refresh' \
--header 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2NvdW50X2lkIjoiYTM3M2ZiYTAtM2Y2MS00NmNjLTk3NGUtNjczMThjZGI2Y2Q2IiwiZXhwIjoxNjcxOTkzNjg1fQ.H7lF3DCRXbg0aK-dS7BL3z_VFnsouEB589JZngjuEBU' \
--header 'Content-Type: application/json' \
--data-raw '{
    "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2NvdW50X2lkIjoiZThlYWRlNzUtOGRiYy00Y2UzLTgyNjAtODJhMDNhN2ZiODM0IiwiZXhwIjoxNjczMjczNTc3fQ.Eujcx3WqfQHs6a8s_dK5vyiFTGXpcBlZEcsf002Fbu4"
}'
```

- account/logout GET : 로그아웃을 진행합니다.  (에제 토큰입니다.)
```shell
curl --location --request GET 'http://127.0.0.1:8000/account/logout' \
--header 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2NvdW50X2lkIjoiZThlYWRlNzUtOGRiYy00Y2UzLTgyNjAtODJhMDNhN2ZiODM0IiwiZXhwIjoxNjcxOTk1MDc1fQ.Bc421MUnzFEFn85VPwkDS_a5oIpRpK4pr5a6uAPo-_8'
```

- money-keep POST : 가계부 생성 합니다.
```shell
curl --location --request POST 'http://127.0.0.1:8000/money-keep' \
--header 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2NvdW50X2lkIjoiZThlYWRlNzUtOGRiYy00Y2UzLTgyNjAtODJhMDNhN2ZiODM0IiwiZXhwIjoxNjcyMzQ4MTk0fQ.jc8xYHAKlJEECtO0wP7us_zGk7J5teAaQ5bllhjIMHg' \
--header 'Content-Type: application/json' \
--data-raw '{
    "memo": "외식먹음",
    "spending": 20000,
    "balance_category": 2,
    "category": 1
}'
```

- money-keep GET : 가계부 전체 리스트 및 액수를 계산하여 가져옵니다.
```shell
curl --location --request GET 'http://127.0.0.1:8000/money-keep' \
--header 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2NvdW50X2lkIjoiZThlYWRlNzUtOGRiYy00Y2UzLTgyNjAtODJhMDNhN2ZiODM0IiwiZXhwIjoxNjcyMzQ3Nzg2fQ.aePmo71yvZGBbe5NMRneV34Dybil9jVhIgI0NiIxlDE'
```

- money-keep/{financial_ledge_id} GET : 가게부 리스트 상세 정보를 확인할 수 있습니다.
```shell
curl --location --request GET 'http://127.0.0.1:8000/money-keep/ebf42083-7e84-4f6a-aa92-04dc725b6ea8' \
--header 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2NvdW50X2lkIjoiZThlYWRlNzUtOGRiYy00Y2UzLTgyNjAtODJhMDNhN2ZiODM0IiwiZXhwIjoxNjcyMzQ4MTk0fQ.jc8xYHAKlJEECtO0wP7us_zGk7J5teAaQ5bllhjIMHg'
```

- money-keep/{financial_ledge_id} PUT : 가게부 상세 정보를 수정합니다.
```shell
curl --location --request PUT 'http://127.0.0.1:8000/money-keep/ebf42083-7e84-4f6a-aa92-04dc725b6ea8' \
--header 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2NvdW50X2lkIjoiZThlYWRlNzUtOGRiYy00Y2UzLTgyNjAtODJhMDNhN2ZiODM0IiwiZXhwIjoxNjcyMzQ4MTk0fQ.jc8xYHAKlJEECtO0wP7us_zGk7J5teAaQ5bllhjIMHg' \
--header 'Content-Type: application/json' \
--data-raw '{
    "memo": "외식",
    "spending": 350000,
    "category": 1,
    "balance_category": 2
}'
```


- money-keep/{financial_ledge_id} DELETE : 가게부 정보를 삭제합니다.
```shell
curl --location --request DELETE 'http://127.0.0.1:8000/money-keep/ebf42083-7e84-4f6a-aa92-04dc725b6ea8' \
--header 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2NvdW50X2lkIjoiZThlYWRlNzUtOGRiYy00Y2UzLTgyNjAtODJhMDNhN2ZiODM0IiwiZXhwIjoxNjcyMzQ4MTk0fQ.jc8xYHAKlJEECtO0wP7us_zGk7J5teAaQ5bllhjIMHg'
```


- money-keep/copy/{financial_ledge_id} POST : 가계부 데이터를 설정값을 복사해서 새로 하나 만들어줍니다.
```shell
curl --location --request POST 'http://127.0.0.1:8000/money-keep/copy/ebf42083-7e84-4f6a-aa92-04dc725b6ea8' \
--header 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2NvdW50X2lkIjoiZThlYWRlNzUtOGRiYy00Y2UzLTgyNjAtODJhMDNhN2ZiODM0IiwiZXhwIjoxNjcyMzQ4MTk0fQ.jc8xYHAKlJEECtO0wP7us_zGk7J5teAaQ5bllhjIMHg'
```

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
