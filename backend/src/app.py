from fastapi import FastAPI

from src.middlewares.error_middleware import app_error_handler
from src.routers import (
    auth_router,
    carrito_router,
    category_router,
    cliente_router,
    compra_router,
    product_router,
    resena_router,
    variante_router,
)
from src.utils.errors import AppError


app = FastAPI(title="Initial Structure API")

app.add_exception_handler(AppError, app_error_handler)

app.include_router(auth_router.router, prefix="/api")
app.include_router(carrito_router.router, prefix="/api")
app.include_router(category_router.router, prefix="/api")
app.include_router(cliente_router.router, prefix="/api")
app.include_router(compra_router.router, prefix="/api")
app.include_router(product_router.router, prefix="/api")
app.include_router(resena_router.router, prefix="/api")
app.include_router(variante_router.router, prefix="/api")


@app.get("/health")
def health():
    return {"status": "ok"}
