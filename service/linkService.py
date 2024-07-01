import random
from fastapi import HTTPException
from fastapi.responses import JSONResponse
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
        existing_link = db_client.local.links.find_one({"url": link_data.url})
        if existing_link:
            # Convertir el objeto Link a un diccionario y devolver con código 200
            return JSONResponse(content=Link(**existing_link).dict(), status_code=200)

        code = self.genCode()
        linkObject = Link(url=link_data.url, short_code=code)
        linkDict = linkObject.dict()
        del linkDict["id"]  # Asumiendo que el ID es generado automáticamente por la base de datos
        try:
            id = db_client.local.links.insert_one(linkDict).inserted_id
            new_link = db_client.local.links.find_one({"_id": id})
            if not new_link:
                raise HTTPException(status_code=404, detail="Link not found after creation")

            # Asegurarse de que el URL es válido y corregir si es necesario
            new_link["url"] = new_link["url"].replace(" ", "")
            if "." in new_link["url"] and not (new_link["url"].startswith("http://") or new_link["url"].startswith("https://")):
                new_link["url"] = "https://" + new_link["url"]

            # Verificar nuevamente la validez del URL
            if "." not in new_link["url"]:
                raise HTTPException(status_code=400, detail="Provide a valid URL")

            # Devolver el nuevo link con código 201
            return JSONResponse(content=Link(**new_link).dict(), status_code=201)

        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    