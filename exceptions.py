from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse


# Custom exceptions
class PincodeNotFoundError(Exception):
    def __init__(self, pincode: str):
        self.pincode = pincode


class InvalidPincodeError(Exception):
    def __init__(
        self,
        pincode: str,
        reason: str = "Invalid Format"
    ):
        self.pincode = pincode
        self.reason = reason


# Exception handler for missing pincodes
async def pincode_not_found_handler(
    request: Request,
    exc: PincodeNotFoundError
):
    return JSONResponse(
        status_code=404,
        content={
            "error": "pincode_not_found",
            "message": f"No location for pincode: {exc.pincode}",
            "pincode": exc.pincode
        }
    )


# Exception handler for invalid pincodes
async def pincode_invalid_handler(
    request: Request,
    exc: InvalidPincodeError
):
    return JSONResponse(
        status_code=400,
        content={
            "error": "invalid_pincode",
            "message": f"Pincode {exc.pincode} is invalid: {exc.reason}",
            "pincode": exc.pincode
        }
    )
