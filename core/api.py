from fastapi import APIRouter

from server.endpoints import router as server_router

router = APIRouter()
router.include_router(server_router, prefix="/file")
