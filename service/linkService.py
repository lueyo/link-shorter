import random
from fastapi import HTTPException
from fastapi.responses import JSONResponse
from db.client import db_client, pwd_context, PASSKEY, SALT
from db.models.link import Link, LinkCreate
from db.schemas.link import link_schema

class LinkService:

    def genCode(self):
        codigo = ""
        length = random.randint(6, 8)
        for _ in range(length):
            char_type = random.choice(['uppercase', 'lowercase', 'number'])
            if char_type == 'uppercase':
                codigo += chr(random.randrange(65, 91))
            elif char_type == 'lowercase':
                codigo += chr(random.randrange(97, 123))
            else:
                codigo += chr(random.randrange(48, 58))
        return codigo

    def hash_password(self, password: str) -> str:
        combined = f"{PASSKEY}{password}{SALT}"
        return pwd_context.hash(combined)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        combined = f"{PASSKEY}{plain_password}{SALT}"
        return pwd_context.verify(combined, hashed_password)

    def createLink(self, link_data: LinkCreate):
        existing_link_no_pass = db_client.local.links.find_one({"url": link_data.url, "password": None})

        if link_data.password:
            existing_with_password = db_client.local.links.find_one({"url": link_data.url, "password": {"$ne": None}})
            if existing_with_password:
                hashed = self.hash_password(link_data.password)
                if existing_with_password.get("password") == hashed:
                    return JSONResponse(content=Link(**existing_with_password).dict(), status_code=200)
            code = self.genCode()
            linkObject = Link(url=link_data.url, short_code=code, password=self.hash_password(link_data.password))
        else:
            if existing_link_no_pass:
                return JSONResponse(content=Link(**existing_link_no_pass).dict(), status_code=200)
            code = self.genCode()
            linkObject = Link(url=link_data.url, short_code=code)

        linkDict = linkObject.dict()
        del linkDict["id"]
        try:
            id = db_client.local.links.insert_one(linkDict).inserted_id
            new_link = db_client.local.links.find_one({"_id": id})
            if not new_link:
                raise HTTPException(status_code=404, detail="Link not found after creation")

            new_link["url"] = new_link["url"].replace(" ", "")
            if "." in new_link["url"] and not (new_link["url"].startswith("http://") or new_link["url"].startswith("https://")):
                new_link["url"] = "https://" + new_link["url"]

            if "." not in new_link["url"]:
                raise HTTPException(status_code=400, detail="Provide a valid URL")

            return JSONResponse(content=Link(**new_link).dict(), status_code=201)

        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    