from fastapi import APIRouter

from fastapi.responses import FileResponse

router = APIRouter(prefix="")


@router.get("/")
async def form():
    
    return FileResponse("static/templates/index.html")