
from uuid import uuid4
from datetime import datetime, timezone

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse

from backend.app.models import (
    ShortenRequest,
    ShortenResponse,
    UrlInfoResponse,
)

from backend.app.database import urls_table


app = FastAPI(
    title="AWS URL Shortener",
    description="API para crear y consultar enlaces cortos",
    version="1.0.0",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500",
        "http://localhost:5500",
        "http://127.0.0.1:8000",
        "http://localhost:8000",
    ],
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type"],
)


@app.get("/")
def home():
    return {
        "message": "AWS URL Shortener API funcionando",
        "docs": "/docs",
    }


@app.post("/shorten", response_model=ShortenResponse)
def shorten_url(request: ShortenRequest):

    short_code = str(uuid4())
    original_url = str(request.original_url)
    created_at = datetime.now(timezone.utc).isoformat()

    # Guardamos el enlace en DynamoDB
    urls_table.put_item(
        Item={
            "short_code": short_code,
            "original_url": original_url,
            "created_at": created_at,
        }
    )

    short_url = f"http://127.0.0.1:8000/{short_code}"

    return ShortenResponse(
        short_code=short_code,
        original_url=original_url,
        short_url=short_url,
    )


@app.get("/urls/{short_code}", response_model=UrlInfoResponse)
def get_url_info(short_code: str):

    # Buscamos el enlace en DynamoDB
    response = urls_table.get_item(
        Key={"short_code": short_code}
    )

    record = response.get("Item")

    if record is None:
        raise HTTPException(
            status_code=404,
            detail="Enlace no encontrado",
        )

    return UrlInfoResponse(**record)


@app.get("/{short_code}")
def redirect_url(short_code: str):

    # Buscamos el enlace en DynamoDB
    response = urls_table.get_item(
        Key={"short_code": short_code}
    )

    record = response.get("Item")

    if record is None:
        raise HTTPException(
            status_code=404,
            detail="Enlace no encontrado",
        )

    return RedirectResponse(
        url=record["original_url"],
        status_code=307,
    )
