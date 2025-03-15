import zoneinfo
from fastapi import FastAPI
from datetime import datetime


app = FastAPI()

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
