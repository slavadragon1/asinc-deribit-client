from fastapi import FastAPI, HTTPException, Query
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError

from main import Ticker


app = FastAPI()

engine = create_engine('postgresql://postgres:root@localhost:5432/Deribit_client')
Session = sessionmaker(bind=engine)
session = Session()


@app.get("/")
async def homepage():
    return {'methods':
       ['/tickers?ticker=',
        '/last_price?ticker=' ,
        '/ticker_by_time&ticker=']}

# Получение всех сохраненных данных по указанной валюте 
@app.get('/tickers')
async def get_all_tickers(ticker: str = Query(...)):
    try:
        tickers = session.query(Ticker).filter_by(ticker=ticker).all()
        if not tickers:
            raise HTTPException(status_code=404, detail='Ticker not found')

        return [{'ticker': t.ticker, 'price': t.price, 'timestamp': t.timestamp} for t in tickers]
        
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail='Database error') from e


# Получение последней цены валюты
@app.get('/last_price') 
async def get_last_price(ticker: str = Query(...)):
    try:
        last_ticker = session.query(Ticker).filter_by(ticker=ticker).order_by(Ticker.timestamp.desc()).first()
        if not last_ticker:
            raise HTTPException(status_code=404, detail='Ticker not found')

        return {'ticker': last_ticker.ticker, 'price': last_ticker.price, 'timestamp': last_ticker.timestamp} 
        
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail='Database error') from e


# Получение цены валюты с фильтром по дате
@app.get('/ticker_by_time')
def get_price_by_time(ticker: str = Query(...), timestamp: int = Query(...)):
    try:
        ticker_data = session.query(Ticker).filter_by(ticker=ticker, timestamp=timestamp).first()
        if not ticker_data:
            raise HTTPException(status_code=404, detail='Ticker not found')

        return {'ticker': ticker_data.ticker, 'price': ticker_data.price, 'timestamp': ticker_data.timestamp}

    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail='Database error') from e