from fastapi import FastAPI, exceptions
from fastapi.responses import JSONResponse
from pydantic import ValidationError
from src.api import admin, chemist, citizen, govt, info, inventory, market, transaction, miner, bids
import json
import logging
import sys
from starlette.middleware.cors import CORSMiddleware

description = """
Novastrum Market is the premier black market for all your susbtance and narcotic desires.
"""

app = FastAPI(
    title="Novastrum Market",
    description=description,
    version="0.0.1",
    terms_of_service="http://example.com/terms/",
    contact={
        "name": "Ethan Swenke",
        "email": "eswenke@calpoly.edu",
    },
)

#origins = ["https://potion-exchange.vercel.app"]

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,
#     allow_credentials=True,
#     allow_methods=["GET", "OPTIONS"],
#     allow_headers=["*"],
# )

app.include_router(inventory.router)
app.include_router(transaction.router)
app.include_router(market.router)
app.include_router(govt.router)
app.include_router(chemist.router)
app.include_router(admin.router)
app.include_router(info.router)
app.include_router(miner.router)
app.include_router(citizen.router)
app.include_router(bids.router)

@app.exception_handler(exceptions.RequestValidationError)
@app.exception_handler(ValidationError)
async def validation_exception_handler(request, exc):
    logging.error(f"The client sent invalid data!: {exc}")
    exc_json = json.loads(exc.json())
    response = {"message": [], "data": None}
    for error in exc_json:
        response['message'].append(f"{error['loc']}: {error['msg']}")

    return JSONResponse(response, status_code=422)

@app.get("/")
async def root():
    return {"message": "Welcome to the Novastrum Market."}
