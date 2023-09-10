from fastapi import APIRouter, Body, Request, HTTPException, status, Depends
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from .models import COCODataMultiple
from motor.motor_asyncio import AsyncIOMotorClient
from config import settings



router = APIRouter()






