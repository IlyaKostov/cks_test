import logging
import os

from dotenv import load_dotenv, find_dotenv
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from app.routers import router as api_roter

logger = logging.getLogger(__name__)


def create_fast_api_app():
    load_dotenv(find_dotenv('.env'))
    env_name = os.getenv('MODE', "DEV")

    if env_name != 'PROD':
        _app = FastAPI(
            default_response_class=ORJSONResponse,
        )
    else:
        _app = FastAPI(
            default_response_class=ORJSONResponse,
            docs_url=None,
            redoc_url=None,
        )

    _app.include_router(api_roter)
    return _app


app = create_fast_api_app()
