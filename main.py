from fastapi import FastAPI
from database import database, product_events, user_events
from pydantic import BaseModel
from typing import List, Optional
from contextlib import asynccontextmanager
import datetime

app = FastAPI()

class ProductEvent(BaseModel):
    id: int
    evt_type: str
    user_id: str
    product_id: str
    location_id: str
    location: str
    evt_date: datetime.datetime
    transaction_id: str
    platform: str
    meta: Optional[str]
    created: datetime.datetime
    last_modified: datetime.datetime
    
class ProductLost(BaseModel):
    product_id: str

class UserEvent(BaseModel):
    id: int
    evt_type: str
    user_id: str
    evt_date: datetime.datetime
    platform: str
    meta: Optional[str]
    created: datetime.datetime
    last_modified: datetime.datetime
    

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize the database connection
    await database.connect()
    yield
    # Close the database connection
    await database.disconnect()


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


@app.get("/product-events/", response_model=List[ProductEvent])
async def read_product_events():
    query = "SELECT * FROM product_events"
    return await database.fetch_all(query)

@app.get("/lost-products/", response_model=List[ProductLost])
async def read_lost_products():
    query = """
    WITH latest_events AS (
    SELECT 
    product_id,
    evt_type,
    evt_date,
    ROW_NUMBER() OVER (PARTITION BY product_id ORDER BY evt_date DESC) as rn
    FROM product_events
    )
    SELECT product_id
    FROM latest_events
    WHERE rn = 1
    AND evt_type = 'borrow'
    AND evt_date <= NOW() - INTERVAL '3 months'
    ORDER BY product_id;
    """
    
    return await database.fetch_all(query)

@app.get("/unreturned-products/", response_model=List[ProductLost])
async def read_unreturned_products():
    query = """
    WITH latest_product_events AS (
    SELECT 
    product_id,
    user_id,
    evt_type,
    ROW_NUMBER() OVER (PARTITION BY product_id ORDER BY evt_date DESC) as rn
    FROM product_events
    ),
    unreturned_borrows AS (
    SELECT product_id, user_id
    FROM latest_product_events
    WHERE rn = 1 AND evt_type = 'borrow'
    ),
    latest_payment_methods AS (
    SELECT 
        user_id,
        meta,
        ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY evt_date DESC) as rn
    FROM user_events
    WHERE evt_type = 'add-payment-method'
    )
    SELECT 
    ub.product_id,
    ub.user_id,
    lpm.meta,
    TO_DATE(SUBSTRING(lpm.meta FROM '"valid_until": "([^"]+)"'), 'MM/YY') as expiration_date
    FROM unreturned_borrows ub
    JOIN latest_payment_methods lpm ON ub.user_id = lpm.user_id
    WHERE lpm.rn = 1
    AND TO_DATE(SUBSTRING(lpm.meta FROM '"valid_until": "([^"]+)"'), 'MM/YY') <= NOW() + INTERVAL '30 days'
    ORDER BY ub.product_id;
    """
    
    return await database.fetch_all(query)

@app.get("/user-events/", response_model=List[UserEvent])
async def read_user_events():
    query = user_events.select()
    return await database.fetch_all(query)