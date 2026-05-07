from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from app.database import Base, engine
from app.routers.auth import router as auth_router
from app.routers.shipment import router as shipment_router
load_dotenv()
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Shipment Tracking API",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:5174",
        "http://127.0.0.1:5174",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(shipment_router)


@app.get("/")
def health():
    return {"status": "ok"}