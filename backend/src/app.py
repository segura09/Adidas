from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.middlewares.error_middleware import app_error_handler
from src.routers import (
    auth_router,
    carrito_router,
    category_router,
    cliente_router,
    compra_router,
    cupon_router,
    devolucion_router,
    product_router,
    report_router,
    resena_router,
    variante_router,
)
from src.utils.errors import AppError


app = FastAPI(title="Initial Structure API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_exception_handler(AppError, app_error_handler)

app.include_router(auth_router.router, prefix="/api")
app.include_router(carrito_router.router, prefix="/api")
app.include_router(category_router.router, prefix="/api")
app.include_router(cliente_router.router, prefix="/api")
app.include_router(compra_router.router, prefix="/api")
app.include_router(cupon_router.router, prefix="/api")
app.include_router(devolucion_router.router, prefix="/api")
app.include_router(product_router.router, prefix="/api")
app.include_router(report_router.router, prefix="/api")
app.include_router(resena_router.router, prefix="/api")
app.include_router(variante_router.router, prefix="/api")


@app.get("/health")
def health():
    return {"status": "ok"}
