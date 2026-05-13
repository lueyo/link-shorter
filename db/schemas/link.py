def link_schema(link) -> dict:
    return {"id": str(link["_id"]), "url": link["url"], "short_code": link["short_code"], "password": link.get("password")}