from fastapi import FastAPI
from routers import linkRouter, mainRouter
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse

app = FastAPI()

#routers
app.include_router(mainRouter.router)
app.include_router(linkRouter.router)

app.mount("/static", StaticFiles(directory="static"), name="static")



