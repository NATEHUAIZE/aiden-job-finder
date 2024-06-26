from typing import Annotated

from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel
from redis.exceptions import ConnectionError

from aiden_scraper import redis_client
from aiden_scraper.scrapers.wtj import scraper as wtj_scraper

app = FastAPI()


class JobOfferRequest(BaseModel):
    location: str
    query: str
    limit: int


@app.get("/health", status_code=200)
def healthcheck() -> dict[str, str]:
    try:
        redis_client.ping()
    except ConnectionError as e:
        raise RuntimeError("Failed to connect to Redis") from e
    return {"status": "healthy"}


@app.post("/scrape", response_model=list[str])
def scrape(job_offer_request: Annotated[JobOfferRequest, Body()]) -> list[str]:
    wtj_results = wtj_scraper.search_jobs(
        search_query=job_offer_request.query, location=job_offer_request.location, num_results=job_offer_request.limit
    )
    # _ = indeed_scraper.search_jobs(
    #     search_query=job_offer_request.query, location=job_offer_request.location, num_results=job_offer_request.limit
    # )
    return wtj_results
