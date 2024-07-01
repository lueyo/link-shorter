from fastapi import FastAPI
from routers import linkRouter
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse

app = FastAPI()

#routers
app.include_router(linkRouter.router)

app.mount("/static", StaticFiles(directory="static"), name="static")



