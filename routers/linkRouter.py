from fastapi import APIRouter, HTTPException, status, Query
from db.models.link import Link, LinkCreate
from db.client import db_client
from service.linkService import LinkService
from db.schemas.link import link_schema
from fastapi.responses import RedirectResponse, FileResponse

router = APIRouter(prefix="/s", responses={status.HTTP_404_NOT_FOUND: {"description": "Not found Link"}})


@router.get("/{short_code}")
async def get_link(short_code: str, password: str = Query(None)):
    link = db_client.local.links.find_one({"short_code": short_code})
    if link:
        if link.get("password"):
            link_service = LinkService()
            if password and link_service.verify_password(password, link["password"]):
                if link["url"].startswith("http"):
                    return RedirectResponse(url=link["url"])
                else:
                    return RedirectResponse(url="https://" + link["url"])
            return FileResponse("static/templates/password.html")
        if link["url"].startswith("http"):
            return RedirectResponse(url=link["url"])
        else:
            return RedirectResponse(url="https://" + link["url"])
    else:
        raise HTTPException(status_code=404, detail="Link not found")


@router.post("/{short_code}/verify")
async def verify_password(short_code: str, password: str = Query(...)):
    link = db_client.local.links.find_one({"short_code": short_code})
    if link:
        if link.get("password"):
            link_service = LinkService()
            if link_service.verify_password(password, link["password"]):
                if link["url"].startswith("http"):
                    return {"valid": True, "url": link["url"]}
                else:
                    return {"valid": True, "url": "https://" + link["url"]}
        return {"valid": False}
    raise HTTPException(status_code=404, detail="Link not found")


@router.post("/", response_model=Link, status_code=status.HTTP_201_CREATED)
async def create_link(link_data: LinkCreate):
    link_service = LinkService()
    link = link_service.createLink(link_data=link_data)
    return link
    
    
    
