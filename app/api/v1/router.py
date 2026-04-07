# app/api/v1/router.py
""" Main API router """

from fastapi import APIRouter
from app.api.v1 import agent

api_router = APIRouter()
api_router.include_router(agent.router, prefix="/agent", tags=["Agent"])