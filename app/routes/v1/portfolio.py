from fastapi import APIRouter
from typing import List, Dict
from app.dto.portifolio import UserRequest, UserResponse


router = APIRouter()

@router.post("/status/")
async def get_portifolio_status() -> List[Dict]:
    pass

@router.get("/health")
async def get_health(user: UserRequest):
    return {"message": "Healthy"}
