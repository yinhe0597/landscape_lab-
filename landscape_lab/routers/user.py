from fastapi import APIRouter, Depends
from controllers.user_controller import router as user_router

router = APIRouter()
router.include_router(user_router, prefix="/api/v1", tags=["users"])
