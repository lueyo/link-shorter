def link_schema(link) -> dict:
    return {"id":str(link["_id"]),"url":link["url"]}