**Plan por HU**

La idea es que cada HU tenga tres bloques: base de datos, backend y frontend. Te dejo qué archivo crear o modificar, y qué funciones o piezas concretas tocar dentro de cada uno.

## HU1 — Alta de categorías y productos

### Base de datos
- Modificar [backend/src/db/tables.sql](/home/facundo/Documents/2026/Adidas/backend/src/db/tables.sql)
- Crear o ajustar la tabla `categorias` con `nombre UNIQUE`
- Crear o ajustar la tabla `productos` con `categoria_id NOT NULL`, `precio_base > 0` y `activo BOOLEAN DEFAULT TRUE`
- Revisar [backend/src/db/models/category_model.py](/home/facundo/Documents/2026/Adidas/backend/src/db/models/category_model.py) y [backend/src/db/models/producto_model.py](/home/facundo/Documents/2026/Adidas/backend/src/db/models/producto_model.py)

### Backend
- Modificar [backend/src/schemas/category_schema.py](/home/facundo/Documents/2026/Adidas/backend/src/schemas/category_schema.py)
- Modificar [backend/src/schemas/product_schema.py](/home/facundo/Documents/2026/Adidas/backend/src/schemas/product_schema.py)
- Crear o completar [backend/src/dtos/product_dto.py](/home/facundo/Documents/2026/Adidas/backend/src/dtos/product_dto.py)
- Crear o completar [backend/src/mappers/product_mapper.py](/home/facundo/Documents/2026/Adidas/backend/src/mappers/product_mapper.py)
- Crear [backend/src/repositories/product_repository.py](/home/facundo/Documents/2026/Adidas/backend/src/repositories/product_repository.py)
- Crear [backend/src/services/product_service.py](/home/facundo/Documents/2026/Adidas/backend/src/services/product_service.py)
- Crear [backend/src/routers/product_router.py](/home/facundo/Documents/2026/Adidas/backend/src/routers/product_router.py)
- Tocar `create_category`, `create_product`, `list_categories`, `list_products`, `update_product` y una baja lógica tipo `deactivate_product`
- Registrar el router en [backend/src/app.py](/home/facundo/Documents/2026/Adidas/backend/src/app.py)

### Frontend
- Crear [frontend/app/(admin)/categories/page.tsx](/home/facundo/Documents/2026/Adidas/frontend/app/(admin)/categories/page.tsx)
- Crear [frontend/app/(admin)/products/page.tsx](/home/facundo/Documents/2026/Adidas/frontend/app/(admin)/products/page.tsx)
- Crear formularios para alta/edición de categoría y producto
- Crear un cliente HTTP en [frontend/app/lib/api.ts](/home/facundo/Documents/2026/Adidas/frontend/app/lib/api.ts)
- Crear una capa simple de acciones de formulario o fetchers para `createCategory`, `createProduct`, `listCategories`, `listProducts`

## HU2 — Variantes de producto

### Base de datos
- Modificar [backend/src/db/tables.sql](/home/facundo/Documents/2026/Adidas/backend/src/db/tables.sql)
- Asegurar `variantes` con `producto_id`, `talle`, `color`, `stock >= 0`, `sku UNIQUE`
- Mantener la unicidad compuesta `(producto_id, talle, color)`
- Revisar [backend/src/db/models/variante_model.py](/home/facundo/Documents/2026/Adidas/backend/src/db/models/variante_model.py)

### Backend
- Crear o completar [backend/src/schemas/variante_schema.py](/home/facundo/Documents/2026/Adidas/backend/src/schemas/variante_schema.py)
- Crear [backend/src/dtos/variante_dto.py](/home/facundo/Documents/2026/Adidas/backend/src/dtos/variante_dto.py)
- Crear [backend/src/mappers/variante_mapper.py](/home/facundo/Documents/2026/Adidas/backend/src/mappers/variante_mapper.py)
- Crear [backend/src/repositories/variante_repository.py](/home/facundo/Documents/2026/Adidas/backend/src/repositories/variante_repository.py)
- Crear [backend/src/services/variante_service.py](/home/facundo/Documents/2026/Adidas/backend/src/services/variante_service.py)
- Crear [backend/src/routers/variante_router.py](/home/facundo/Documents/2026/Adidas/backend/src/routers/variante_router.py)
- Implementar `create_variant`, `list_variants_by_product`, `update_stock` y validación de SKU único

### Frontend
- Crear [frontend/app/(admin)/products/[id]/variants/page.tsx](/home/facundo/Documents/2026/Adidas/frontend/app/(admin)/products/[id]/variants/page.tsx)
- Crear [frontend/app/components/variant-form.tsx](/home/facundo/Documents/2026/Adidas/frontend/app/components/variant-form.tsx)
- Mostrar listado de variantes por producto con talle, color, stock y SKU
- Agregar acciones para alta y edición de variantes

## HU3 — Buscar productos

### Base de datos
- Revisar [backend/src/db/tables.sql](/home/facundo/Documents/2026/Adidas/backend/src/db/tables.sql) para garantizar índices útiles en `categoria_id`, `talle`, `color` y `stock`
- Verificar relaciones entre `productos` y `variantes`

### Backend
- Modificar [backend/src/routers/product_router.py](/home/facundo/Documents/2026/Adidas/backend/src/routers/product_router.py)
- Modificar [backend/src/repositories/product_repository.py](/home/facundo/Documents/2026/Adidas/backend/src/repositories/product_repository.py)
- Modificar [backend/src/services/product_service.py](/home/facundo/Documents/2026/Adidas/backend/src/services/product_service.py)
- Agregar función `search_products(categoria, talle, color)`
- Asegurar que `list_products` filtre solo `activo = true` y variantes con `stock > 0`

### Frontend
- Crear [frontend/app/(customer)/productos/page.tsx](/home/facundo/Documents/2026/Adidas/frontend/app/(customer)/productos/page.tsx)
- Crear [frontend/app/components/product-filters.tsx](/home/facundo/Documents/2026/Adidas/frontend/app/components/product-filters.tsx)
- Leer query params `categoria`, `talle`, `color`
- Mostrar solo productos que devuelva el backend con stock disponible

## HU4 — Cupones de descuento

### Base de datos
- Modificar [backend/src/db/tables.sql](/home/facundo/Documents/2026/Adidas/backend/src/db/tables.sql)
- Crear o ajustar la tabla `cupones` con `codigo UNIQUE`, `porcentaje_descuento` entre 1 y 100, `fecha_vencimiento`, `usos_maximos`, `usos_actuales`
- Revisar [backend/src/db/models/cupon_model.py](/home/facundo/Documents/2026/Adidas/backend/src/db/models/cupon_model.py)

### Backend
- Crear o completar [backend/src/schemas/cupon_schema.py](/home/facundo/Documents/2026/Adidas/backend/src/schemas/cupon_schema.py)
- Crear [backend/src/dtos/cupon_dto.py](/home/facundo/Documents/2026/Adidas/backend/src/dtos/cupon_dto.py)
- Crear [backend/src/mappers/cupon_mapper.py](/home/facundo/Documents/2026/Adidas/backend/src/mappers/cupon_mapper.py)
- Crear [backend/src/repositories/cupon_repository.py](/home/facundo/Documents/2026/Adidas/backend/src/repositories/cupon_repository.py)
- Crear [backend/src/services/cupon_service.py](/home/facundo/Documents/2026/Adidas/backend/src/services/cupon_service.py)
- Crear [backend/src/routers/cupon_router.py](/home/facundo/Documents/2026/Adidas/backend/src/routers/cupon_router.py)
- Implementar `create_coupon`, `validate_coupon`, `consume_coupon_use`

### Frontend
- Crear [frontend/app/(admin)/cupones/page.tsx](/home/facundo/Documents/2026/Adidas/frontend/app/(admin)/cupones/page.tsx)
- Crear [frontend/app/components/coupon-form.tsx](/home/facundo/Documents/2026/Adidas/frontend/app/components/coupon-form.tsx)
- Agregar campo para aplicar cupón en checkout

## HU5 — Crear compra

### Base de datos
- Modificar [backend/src/db/tables.sql](/home/facundo/Documents/2026/Adidas/backend/src/db/tables.sql)
- Asegurar tablas `compras` y `compra_items` con `precio_unitario` guardado al momento de compra
- Revisar [backend/src/db/models/compra_model.py](/home/facundo/Documents/2026/Adidas/backend/src/db/models/compra_model.py) y [backend/src/db/models/compra_items_model.py](/home/facundo/Documents/2026/Adidas/backend/src/db/models/compra_items_model.py)

### Backend
- Modificar [backend/src/schemas/product_schema.py](/home/facundo/Documents/2026/Adidas/backend/src/schemas/product_schema.py) o crear un schema específico de checkout si hace falta
- Crear [backend/src/dtos/compra_dto.py](/home/facundo/Documents/2026/Adidas/backend/src/dtos/compra_dto.py)
- Crear [backend/src/mappers/compra_mapper.py](/home/facundo/Documents/2026/Adidas/backend/src/mappers/compra_mapper.py)
- Crear [backend/src/repositories/compra_repository.py](/home/facundo/Documents/2026/Adidas/backend/src/repositories/compra_repository.py)
- Crear [backend/src/services/compra_service.py](/home/facundo/Documents/2026/Adidas/backend/src/services/compra_service.py)
- Crear [backend/src/routers/compra_router.py](/home/facundo/Documents/2026/Adidas/backend/src/routers/compra_router.py)
- Implementar `create_purchase`, `validate_stock_for_items`, `reserve_stock`, `save_purchase_items`, `calculate_total`
- Hacer que todo corra en una transacción única

### Frontend
- Crear [frontend/app/(customer)/checkout/page.tsx](/home/facundo/Documents/2026/Adidas/frontend/app/(customer)/checkout/page.tsx)
- Crear [frontend/app/components/checkout-summary.tsx](/home/facundo/Documents/2026/Adidas/frontend/app/components/checkout-summary.tsx)
- Mostrar subtotal, descuento, total final y botón de confirmar compra

## HU6 — Aplicar cupón en la compra

### Base de datos
- Verificar que `compras.cupon_id` exista y permita nulos
- Verificar incremento de `usos_actuales` al confirmar la compra

### Backend
- Modificar [backend/src/services/compra_service.py](/home/facundo/Documents/2026/Adidas/backend/src/services/compra_service.py)
- Modificar [backend/src/services/cupon_service.py](/home/facundo/Documents/2026/Adidas/backend/src/services/cupon_service.py)
- Agregar funciones `apply_coupon_to_purchase`, `recalculate_total_with_discount`, `increment_coupon_use_on_confirm`
- Rechazar cupón vencido o sin usos disponibles

### Frontend
- Agregar input de cupón en [frontend/app/(customer)/checkout/page.tsx](/home/facundo/Documents/2026/Adidas/frontend/app/(customer)/checkout/page.tsx)
- Mostrar el descuento calculado antes de confirmar

## HU7 — Descuento de stock

### Base de datos
- Asegurar que `compras.estado` tenga solo los estados válidos
- Revisar triggers solo si después querés mover parte de la lógica a base, aunque no es obligatorio para este plan

### Backend
- Modificar [backend/src/services/compra_service.py](/home/facundo/Documents/2026/Adidas/backend/src/services/compra_service.py)
- Crear o completar funciones `mark_purchase_as_paid`, `mark_purchase_as_cancelled`, `mark_purchase_as_shipped`, `mark_purchase_as_delivered`
- Agregar lógica de `decrease_stock_on_payment` y `restore_stock_on_cancel`
- Rechazar transiciones inválidas de estado

### Frontend
- Crear [frontend/app/(customer)/compras/[id]/page.tsx](/home/facundo/Documents/2026/Adidas/frontend/app/(customer)/compras/[id]/page.tsx)
- Mostrar estado de la compra y acciones válidas según estado

## HU8 — Historial del cliente

### Base de datos
- Verificar índices en `compras.cliente_id` y `compras.fecha`
- Asegurar relación entre compras, items y cliente

### Backend
- Modificar [backend/src/routers/user_router.py](/home/facundo/Documents/2026/Adidas/backend/src/routers/user_router.py) o crear [backend/src/routers/cliente_router.py](/home/facundo/Documents/2026/Adidas/backend/src/routers/cliente_router.py) si querés separar mejor el dominio
- Crear o completar [backend/src/services/cliente_service.py](/home/facundo/Documents/2026/Adidas/backend/src/services/cliente_service.py)
- Crear [backend/src/repositories/cliente_repository.py](/home/facundo/Documents/2026/Adidas/backend/src/repositories/cliente_repository.py)
- Crear DTOs y mappers para compras con items anidados
- Implementar `get_customer_purchases(cliente_id, estado=None)` ordenado por fecha descendente

### Frontend
- Crear [frontend/app/(customer)/compras/page.tsx](/home/facundo/Documents/2026/Adidas/frontend/app/(customer)/compras/page.tsx)
- Crear [frontend/app/components/purchase-card.tsx](/home/facundo/Documents/2026/Adidas/frontend/app/components/purchase-card.tsx)
- Agregar filtro por estado

## HU9 — Productos más vendidos

### Base de datos
- Verificar joins entre `compras`, `compra_items` y `productos`
- Asegurar que la consulta filtre solo compras `pagada`, `enviada` y `entregada`

### Backend
- Modificar [backend/src/routers/product_router.py](/home/facundo/Documents/2026/Adidas/backend/src/routers/product_router.py)
- Agregar función `get_top_selling_products(limit=10)` en [backend/src/repositories/product_repository.py](/home/facundo/Documents/2026/Adidas/backend/src/repositories/product_repository.py)
- Exponer un endpoint `GET /productos/top` en el router
- Devolver cantidad total vendida y facturación acumulada por producto

### Frontend
- Crear [frontend/app/(admin)/reportes/top-productos/page.tsx](/home/facundo/Documents/2026/Adidas/frontend/app/(admin)/reportes/top-productos/page.tsx)
- Crear tabla con ranking, unidades y facturación

## HU10 — Stock bajo

### Base de datos
- Verificar índice en `variantes.stock`
- Mantener join con producto para mostrar contexto

### Backend
- Crear [backend/src/routers/variante_router.py](/home/facundo/Documents/2026/Adidas/backend/src/routers/variante_router.py) si no se reutiliza el de variantes ya creado en HU2
- Agregar función `get_low_stock_variants(umbral)` en [backend/src/repositories/variante_repository.py](/home/facundo/Documents/2026/Adidas/backend/src/repositories/variante_repository.py)
- Exponer `GET /variantes/stock-bajo?umbral=5`

### Frontend
- Crear [frontend/app/(admin)/stock-bajo/page.tsx](/home/facundo/Documents/2026/Adidas/frontend/app/(admin)/stock-bajo/page.tsx)
- Mostrar variantes ordenadas por stock ascendente

## HU11 — Carrito persistente

### Base de datos
- Crear o ajustar tablas `carritos` y `carrito_items` en [backend/src/db/tables.sql](/home/facundo/Documents/2026/Adidas/backend/src/db/tables.sql)
- Agregar unicidad de carrito por cliente y PK compuesta en items
- Verificar [backend/src/db/models/carrito_model.py](/home/facundo/Documents/2026/Adidas/backend/src/db/models/carrito_model.py)

### Backend
- Crear [backend/src/schemas/carrito_schema.py](/home/facundo/Documents/2026/Adidas/backend/src/schemas/carrito_schema.py)
- Crear [backend/src/dtos/carrito_dto.py](/home/facundo/Documents/2026/Adidas/backend/src/dtos/carrito_dto.py)
- Crear [backend/src/mappers/carrito_mapper.py](/home/facundo/Documents/2026/Adidas/backend/src/mappers/carrito_mapper.py)
- Crear [backend/src/repositories/carrito_repository.py](/home/facundo/Documents/2026/Adidas/backend/src/repositories/carrito_repository.py)
- Crear [backend/src/services/carrito_service.py](/home/facundo/Documents/2026/Adidas/backend/src/services/carrito_service.py)
- Crear [backend/src/routers/carrito_router.py](/home/facundo/Documents/2026/Adidas/backend/src/routers/carrito_router.py)
- Implementar `add_item_to_cart`, `get_cart`, `clear_cart`, `checkout_from_cart`
- Validar stock disponible al agregar

### Frontend
- Crear [frontend/app/(customer)/carrito/page.tsx](/home/facundo/Documents/2026/Adidas/frontend/app/(customer)/carrito/page.tsx)
- Crear [frontend/app/components/cart-item.tsx](/home/facundo/Documents/2026/Adidas/frontend/app/components/cart-item.tsx)
- Mostrar subtotales y total calculado

## HU12 — Reseñas de productos

### Base de datos
- Crear tabla `resenas` en [backend/src/db/tables.sql](/home/facundo/Documents/2026/Adidas/backend/src/db/tables.sql)
- Agregar unicidad por `cliente_id + producto_id`
- Verificar relación con compras entregadas

### Backend
- Crear [backend/src/db/models/resena_model.py](/home/facundo/Documents/2026/Adidas/backend/src/db/models/resena_model.py)
- Crear [backend/src/schemas/resena_schema.py](/home/facundo/Documents/2026/Adidas/backend/src/schemas/resena_schema.py)
- Crear [backend/src/dtos/resena_dto.py](/home/facundo/Documents/2026/Adidas/backend/src/dtos/resena_dto.py)
- Crear [backend/src/mappers/resena_mapper.py](/home/facundo/Documents/2026/Adidas/backend/src/mappers/resena_mapper.py)
- Crear [backend/src/repositories/resena_repository.py](/home/facundo/Documents/2026/Adidas/backend/src/repositories/resena_repository.py)
- Crear [backend/src/services/resena_service.py](/home/facundo/Documents/2026/Adidas/backend/src/services/resena_service.py)
- Crear [backend/src/routers/resena_router.py](/home/facundo/Documents/2026/Adidas/backend/src/routers/resena_router.py)
- Implementar `create_or_update_review`, `list_reviews_by_product`, `get_product_review_summary`

### Frontend
- Crear [frontend/app/(customer)/productos/[id]/page.tsx](/home/facundo/Documents/2026/Adidas/frontend/app/(customer)/productos/[id]/page.tsx)
- Crear [frontend/app/components/review-form.tsx](/home/facundo/Documents/2026/Adidas/frontend/app/components/review-form.tsx)
- Mostrar promedio y cantidad de reseñas
- Mostrar lista de reseñas más recientes

## HU13 — Devoluciones

### Base de datos
- Crear tablas `devoluciones` y `devolucion_items` en [backend/src/db/tables.sql](/home/facundo/Documents/2026/Adidas/backend/src/db/tables.sql)
- Agregar estado de devolución y vínculo con compra e ítems
- Definir qué datos se guardan para impedir la devolución repetida de los mismos ítems

### Backend
- Crear [backend/src/db/models/devolucion_model.py](/home/facundo/Documents/2026/Adidas/backend/src/db/models/devolucion_model.py)
- Crear [backend/src/db/models/devolucion_item_model.py](/home/facundo/Documents/2026/Adidas/backend/src/db/models/devolucion_item_model.py)
- Crear [backend/src/schemas/devolucion_schema.py](/home/facundo/Documents/2026/Adidas/backend/src/schemas/devolucion_schema.py)
- Crear [backend/src/dtos/devolucion_dto.py](/home/facundo/Documents/2026/Adidas/backend/src/dtos/devolucion_dto.py)
- Crear [backend/src/mappers/devolucion_mapper.py](/home/facundo/Documents/2026/Adidas/backend/src/mappers/devolucion_mapper.py)
- Crear [backend/src/repositories/devolucion_repository.py](/home/facundo/Documents/2026/Adidas/backend/src/repositories/devolucion_repository.py)
- Crear [backend/src/services/devolucion_service.py](/home/facundo/Documents/2026/Adidas/backend/src/services/devolucion_service.py)
- Crear [backend/src/routers/devolucion_router.py](/home/facundo/Documents/2026/Adidas/backend/src/routers/devolucion_router.py)
- Implementar `request_return`, `approve_return`, `reject_return`, `mark_return_reintegrated`
- Reponer stock solo al pasar a reintegrada

### Frontend
- Crear [frontend/app/(customer)/compras/[id]/devolucion/page.tsx](/home/facundo/Documents/2026/Adidas/frontend/app/(customer)/compras/[id]/devolucion/page.tsx)
- Crear [frontend/app/components/return-form.tsx](/home/facundo/Documents/2026/Adidas/frontend/app/components/return-form.tsx)
- Permitir seleccionar ítems específicos de la compra

## HU14 — Reporte de facturación

### Base de datos
- Verificar que las consultas puedan agrupar por categoría a partir de `productos.categoria_id`
- Asegurar que las devoluciones reintegradas restan del total del período

### Backend
- Crear [backend/src/routers/report_router.py](/home/facundo/Documents/2026/Adidas/backend/src/routers/report_router.py)
- Crear [backend/src/services/report_service.py](/home/facundo/Documents/2026/Adidas/backend/src/services/report_service.py)
- Crear [backend/src/repositories/report_repository.py](/home/facundo/Documents/2026/Adidas/backend/src/repositories/report_repository.py)
- Implementar `get_billing_report(desde, hasta)`
- Devolver total facturado, cantidad de compras y desglose por categoría

### Frontend
- Crear [frontend/app/(admin)/reportes/facturacion/page.tsx](/home/facundo/Documents/2026/Adidas/frontend/app/(admin)/reportes/facturacion/page.tsx)
- Crear [frontend/app/components/date-range-filter.tsx](/home/facundo/Documents/2026/Adidas/frontend/app/components/date-range-filter.tsx)
- Mostrar resumen, desglose y totales ajustados por devoluciones

## Base transversal que vas a tocar sí o sí
- Modificar [backend/src/app.py](/home/facundo/Documents/2026/Adidas/backend/src/app.py) para registrar todos los routers nuevos
- Revisar [backend/src/utils/errors.py](/home/facundo/Documents/2026/Adidas/backend/src/utils/errors.py) y [backend/src/middlewares/error_middleware.py](/home/facundo/Documents/2026/Adidas/backend/src/middlewares/error_middleware.py) si hace falta agregar errores nuevos
- Revisar [backend/src/db/connection.py](/home/facundo/Documents/2026/Adidas/backend/src/db/connection.py) para decidir si `create_all` se mantiene o se reemplaza por migraciones
- Crear [frontend/app/lib/api.ts](/home/facundo/Documents/2026/Adidas/frontend/app/lib/api.ts) para centralizar requests
- Crear [frontend/app/lib/auth.ts](/home/facundo/Documents/2026/Adidas/frontend/app/lib/auth.ts) para token y usuario
- Crear [frontend/app/(auth)/login/page.tsx](/home/facundo/Documents/2026/Adidas/frontend/app/(auth)/login/page.tsx) para acceso inicial
- Crear [frontend/app/(admin)/layout.tsx](/home/facundo/Documents/2026/Adidas/frontend/app/(admin)/layout.tsx) y [frontend/app/(customer)/layout.tsx](/home/facundo/Documents/2026/Adidas/frontend/app/(customer)/layout.tsx) para separar navegación por rol
