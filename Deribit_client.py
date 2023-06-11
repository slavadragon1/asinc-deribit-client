import asyncio
import aiohttp
from sqlalchemy import create_engine, Column, Integer, String, Float, BigInteger
from sqlalchemy.orm import declarative_base, sessionmaker


Base = declarative_base() # init db

class Ticker(Base):
    __tablename__ = 'tickers'

    id = Column(Integer, primary_key=True, autoincrement=True)
    ticker = Column(String)
    price = Column(Float)
    timestamp = Column(BigInteger)

async def fetch_ticker(session, symbol):
    url = f'https://www.deribit.com/api/v2/public/get_index_price?index_name={symbol}'
    async with session.get(url) as response:
        data = await response.json()
        return data

async def save_ticker(session, symbol, price, timestamp):
    ticker = Ticker(ticker=symbol, price=price, timestamp=timestamp)
    session.add(ticker)
    session.commit()

async def get_prices():
    symbols = ['btc_usd', 'eth_usd']
    engine = create_engine('postgresql://postgres:root@localhost:5432/Deribit_client')
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session_db = Session()

    async with aiohttp.ClientSession() as session:
        while True:
            for symbol in symbols:
                ticker_data = await fetch_ticker(session, symbol)
                price = ticker_data['result']['index_price']
                timestamp = ticker_data['usOut']

                await save_ticker(session_db, symbol, price, timestamp)
                print(session, symbol, price, timestamp)
            await asyncio.sleep(60)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(get_prices())