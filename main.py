import zoneinfo
from fastapi import FastAPI
from datetime import datetime
from db import SessionDep, create_all_tables
from models import Customer, CustomerCreate, Transaction, Invoice
from sqlmodel import select

app = FastAPI(lifespan=create_all_tables)

country_timezones = {
    "AR": "America/Argentina/Buenos_Aires",
    "BR": "America/Sao_Paulo",
    "CO": "America/Bogota",
    "MX": "America/Mexico_City",
    "PE": "America/Lima",
}

format_codes = {
    "24" : "%H:%M:%S",
    "12" : "%I:%M:%S %p"
}

@app.get("/")
async def read_root():
    return {"message": "Hello, World!"}


@app.get('/time/{iso_code}')
async def time(iso_code: str):
    iso = iso_code.upper()
    timezone_str = country_timezones.get(iso)
    tz = zoneinfo.ZoneInfo(timezone_str)
    return {"time": datetime.now(tz).isoformat()}


@app.get('/time/{iso_code}/{format}')
async def time_format(iso_code: str, format: str):
    iso = iso_code.upper()
    timezone_str = country_timezones.get(iso)
    tz = zoneinfo.ZoneInfo(timezone_str)
    return {"time": datetime.now(tz).strftime(format_codes.get(format))}

db_customers: list[Customer] = []


@app.get('/customer/{id}', response_model=Customer)
async def get_customer(id: str, session: SessionDep):
    return session.exec(select(Customer).where(Customer.id == id)).first()
    #return db_customers[int(id) - 1]

@app.post('/customer', response_model=Customer)
async def create_customer(customer_data: CustomerCreate, session: SessionDep):
    customer = Customer.model_validate(customer_data.model_dump())
    session.add(customer)
    session.commit()
    session.refresh(customer)
    #db_customers.append(customer_data.model_dump())
    
    return customer
    

@app.post('/transactions', response_model=Transaction)
async def create_customer(transaction_data: Transaction):
    return transaction_data

@app.post('/invoices', response_model=Invoice)
async def create_customer(invoice_data: Invoice):
    return invoice_data
