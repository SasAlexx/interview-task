import uvicorn
from fastapi import FastAPI
from database import engine, Base
from router import credits as CreditRouter, plans as PlanRouter, years as YearRouter


Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(CreditRouter.router, prefix='/credits')
app.include_router(PlanRouter.router)
app.include_router(YearRouter.router)

if __name__ == '__main__':
    uvicorn.run('main:app', reload=True)
