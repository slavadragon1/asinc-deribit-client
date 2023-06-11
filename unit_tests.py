from main import get_prices 
from main import save_ticker
from main import Ticker, Base

import asyncio
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine('postgresql://postgres:root@localhost:5432/Deribit_client')
Session = sessionmaker(bind=engine)
session = Session()

# Проверка записи
# записываем в базу тестовые значения, сравниваем с последней записью, удаляем строку
@pytest.mark.asyncio
async def test_get_prices():
    await save_ticker(session, 'Test', 1, 1)
    last_ticker = session.query(Ticker).order_by(Ticker.id.desc()).first()
    
    assert last_ticker.ticker == 'Test'
    assert last_ticker.price == 1
    assert last_ticker.timestamp == 1
    session.query(Ticker).filter_by(ticker='Test').delete()
    session.commit()
