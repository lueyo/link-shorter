from fastapi import APIRouter, HTTPException, status, FastAPI
from db.models.link import Link, LinkCreate
from db.client import db_client
from service.linkService import LinkService
from db.schemas.link import link_schema
from db.client import db_client
from fastapi.responses import RedirectResponse , FileResponse

router = APIRouter(prefix="", responses={status.HTTP_404_NOT_FOUND: {"description": "Not found Link"}})




@router.get("/")
async def form():
    
    return FileResponse("static/templates/index.html")

@router.get("/{short_code}")
async def get_link(short_code: str):
    link = db_client.local.links.find_one({"short_code": short_code})
    if link:
        # returns the redirect to the original url
        if link["url"].startswith("http"):
            return RedirectResponse(url=link["url"])
        else:
            
            return RedirectResponse(url="https://"+link["url"])
        #return link_schema(link)
    else:
        raise HTTPException(status_code=404, detail="Link not found")



@router.post("/", response_model=Link, status_code=status.HTTP_201_CREATED)
async def create_link(link_data: LinkCreate):
    link_service = LinkService()  # Create an instance of LinkService
    link = link_service.createLink(link_data=link_data)
    return link
    
    
    
