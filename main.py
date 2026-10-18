from fastapi import FastAPI
from exceptions import (
    PincodeNotFoundError,
    pincode_not_found_handler,
    InvalidPincodeError,
    pincode_invalid_handler
)
from models import LocationResponse,BulkResponse,BulkRequest
from data import pincode_db

app=FastAPI(title="Pincode Lookup API",
            description="Auto Fill City and State from indian Pincode during Checkout")

# register exception handlers
app.add_exception_handler(PincodeNotFoundError,pincode_not_found_handler)
app.add_exception_handler(InvalidPincodeError,pincode_invalid_handler)

@app.get("/")
def read_root():
    return {
        "message":"App Running successfully",
        "status":"Healthy"
    }
    
@app.get("/pincode/{code}", response_model=LocationResponse)
def lookup_pincode(code:str):
    if len(code) != 6 or not code.isdigit():
        raise InvalidPincodeError(code, "Must be exactly 6 digit")
    
    if code not in pincode_db:
        raise PincodeNotFoundError(code)
    return pincode_db[code]

@app.post("/pincode/bulk", response_model=BulkResponse)
def bulk_lookup(request: BulkRequest):
    results = []
    missing = []

    for code in request.pincodes:
        if code in pincode_db:
            results.append(pincode_db[code])
        else:
            missing.append(code)
    
    return BulkResponse(
        found=len(results),
        not_found=len(missing),
        results=results,
        missing=missing
    )

