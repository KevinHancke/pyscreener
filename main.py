from fastapi import FastAPI, Depends, Request, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.responses import JSONResponse
from sqlalchemy import text, func
from sqlalchemy.orm import Session
from models import ItemDB
from database import engine, SessionLocal
from get_data import get_new_rows, append_new_rows
import logging

logger = logging.getLogger(__name__)

app = FastAPI()

templates = Jinja2Templates(directory="templates")

ItemDB.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally: db.close()

async def handle_server_errors(request: Request, exc: Exception):
    logger.exception("Internal Server Error")
    return JSONResponse(status_code=500, content={"message": "Internal Server Error"})

@app.exception_handler(Exception)
async def handle_exception(request: Request, exc: Exception):
    # If you have a custom exception handler, use it here
    return await handle_server_errors(request, exc)

async def fetch_data(request: Request, db: Session=Depends(get_db)):
    try:
        get_new_rows(engine)  # Assuming get_rows is an asynchronous function
        append_new_rows(engine)

        items = db.query(ItemDB).order_by(ItemDB.Datetime.desc()).limit(50).all()
        data = [
            {
                "datetime": str(item.Datetime),
                "open": item.Close,
                "high": item.High,
                "low": item.Low,
                "close": item.Close
            } 
            for item in items
        ]


        #This way works to get data from the ItemDB model
        """ items = db.query(ItemDB).order_by(ItemDB.Datetime.desc()).limit(50).all()
        data = [{"datetime": str(item.Datetime), "close": item.Close} for item in items]"""

        #One way of getting data directly through SQL and works
        """query = text("SELECT Datetime, Close FROM btc_1m ORDER BY Datetime DESC LIMIT 50")
        items = db.execute(query).fetchall()
        data = [{"datetime": str(item[0]), "close": item[1]} for item in items]"""
    

        

        return templates.TemplateResponse("graph.html", {"request": request, "data": data})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

@app.get("/")
async def get_sql_table(request: Request, db: Session = Depends(get_db)):
    return await fetch_data(request, db)

"""@app.get("/")
async def get_sql_table(request: Request, db: Session = Depends(get_db)):
    try:
        await get_rows(db)
        items = db.query(models.ItemDB).limit(50).all()
        date_list = [item.Datetime.isoformat() for item in items]
        close_list = [item.Close for item in items]
        data = {"dates": date_list, "close_values": close_list}

        return templates.TemplateResponse("graph.html", {"request": request, "data": data})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")"""