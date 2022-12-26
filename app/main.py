from fastapi import FastAPI

from config.database import Base, engine
from router import account, money_keep

Base.metadata.create_all(bind=engine)


app = FastAPI(version=0.3)

app.include_router(account.router)
app.include_router(money_keep.router)


@app.get("/")
async def root():
    return {"message": "Hello"}
