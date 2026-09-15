from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from .database import Base, engine, SessionLocal
from . import models
from .routers import auth_router, products, cart, orders, payment
from .seed import seed_products

# backend/app/main.py -> repo_root/frontend
# In Docker this resolves to /app/frontend (see Dockerfile layout); locally
# it resolves to <repo>/frontend, so the app runs the same way in both.
FRONTEND_DIR = Path(__file__).resolve().parent.parent.parent / "frontend"

app = FastAPI(title="Food Delivery Shop API", version="0.1.0")

Base.metadata.create_all(bind=engine)

with SessionLocal() as db:
    seed_products(db)

app.include_router(auth_router.router)
app.include_router(products.router)
app.include_router(cart.router)
app.include_router(orders.router)
app.include_router(payment.router)

app.mount("/static", StaticFiles(directory=str(FRONTEND_DIR / "static")), name="static")


@app.get("/")
def serve_index():
    return FileResponse(str(FRONTEND_DIR / "templates" / "index.html"))


@app.get("/cart.html")
def serve_cart():
    return FileResponse(str(FRONTEND_DIR / "templates" / "cart.html"))


@app.get("/checkout.html")
def serve_checkout():
    return FileResponse(str(FRONTEND_DIR / "templates" / "checkout.html"))


@app.get("/login.html")
def serve_login():
    return FileResponse(str(FRONTEND_DIR / "templates" / "login.html"))


@app.get("/orders.html")
def serve_orders():
    return FileResponse(str(FRONTEND_DIR / "templates" / "orders.html"))


@app.get("/health")
def health_check():
    return {"status": "ok"}
