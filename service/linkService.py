import random
from fastapi import HTTPException
from db.client import db_client
from db.models.link import Link, LinkCreate
from db.schemas.link import link_schema
class LinkService:


    def genCode(self):
        codigo = ""
        for _ in range(11):
            char_type = random.choice(['uppercase', 'lowercase', 'number'])
            if char_type == 'uppercase':
                codigo += chr(random.randrange(65, 91))
            elif char_type == 'lowercase':
                codigo += chr(random.randrange(97, 123))
            else:  
                codigo += chr(random.randrange(48, 58))
        return codigo
    
    def createLink(self, link_data: LinkCreate):
        code = self.genCode()
        print(code)
        linkObject = Link(url=link_data.url, short_code=code)
        linkDict = linkObject.dict()
        del linkDict["id"]
        try:
            id = db_client.local.links.insert_one(linkDict).inserted_id
            new_link = db_client.local.links.find_one({"_id": id})
            if not new_link:
                raise HTTPException(status_code=404, detail="Link not found after creation")
            
            new_link["url"] = new_link["url"].replace(" ", "")
            if new_link["url"].find(".") != -1:
                if new_link["url"].startswith("http://") or new_link["url"].startswith("https://"):
                    return Link(**new_link)
                else:
                    new_link["url"] = "https://" + new_link["url"]
                    return Link(**new_link)
            else:
                raise HTTPException(status_code=400, detail="Provide a valid URL")

        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    