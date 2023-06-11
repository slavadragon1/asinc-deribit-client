from main import get_prices 
from main import save_ticker
from main import Ticker, fetch_ticker

import pytest
import aiohttp
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine('postgresql://postgres:root@localhost:5432/Deribit_client')
Session = sessionmaker(bind=engine)
session = Session()

# Проверка записи
# записываем в базу тестовые значения, сравниваем с последней записью, удаляем строку
@pytest.mark.asyncio
async def test_save_ticker():
    await save_ticker(session, 'Test', 1, 1) # запись тестовой строки
    last_ticker = session.query(Ticker).order_by(Ticker.id.desc()).first() # чтение последней добавленной строки (тестовой)
    
    # сравнение тестовых значений
    assert last_ticker.ticker == 'Test'
    assert last_ticker.price == 1
    assert last_ticker.timestamp == 1
    session.query(Ticker).filter_by(ticker='Test').delete()
    session.commit()

# проверка на заполненность приходящих данных
@pytest.mark.asyncio
async def test_fetch_tickers():
    symbols = ['btc_usd', 'eth_usd']
    client_session = aiohttp.ClientSession()
    for symbol in symbols:
        ticker_data = await fetch_ticker(client_session, symbol)
        assert bool(ticker_data['result']['index_price']) is not False
        assert bool(ticker_data['usOut']) is not False

