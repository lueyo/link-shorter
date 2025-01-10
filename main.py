from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import linkRouter, mainRouter
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse

app = FastAPI()

# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permitir todas las orígenes; ajusta esto según tus necesidades
    allow_credentials=True,
    allow_methods=["*"],  # Permitir todos los métodos HTTP
    allow_headers=["*"],  # Permitir todos los encabezados
)

# Routers
app.include_router(mainRouter.router)
app.include_router(linkRouter.router)

# Archivos estáticos
app.mount("/static", StaticFiles(directory="static"), name="static")
