from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from . import models, database, routes
app = FastAPI()
app.include_router(routes.router)
models.Base.metadata.create_all(bind=database.engine)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)