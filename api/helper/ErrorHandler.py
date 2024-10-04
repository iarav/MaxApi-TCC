from fastapi import HTTPException
from typing import Any

def handleError(response: Any) -> None:
    if isinstance(response, dict) and response.get("error"):
        raise HTTPException(status_code=500, detail=response.get("error"))

def handleException(e: Exception) -> None:
    print("ERROR: ")
    print(e)
    if isinstance(e, HTTPException):
        raise e
    raise HTTPException(status_code=500, detail=str(e))