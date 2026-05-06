-- 1. categorias (HU1)
CREATE TABLE categorias (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL UNIQUE,
    descripcion TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. productos (HU1)
CREATE TABLE productos (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(150) NOT NULL,
    descripcion TEXT,
    precio_base DECIMAL(10,2) NOT NULL CHECK (precio_base > 0),
    categoria_id INT NOT NULL,
    activo BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_categoria FOREIGN KEY (categoria_id) REFERENCES categorias(id)
);

-- 3. variantes (HU2)
CREATE TABLE variantes (
    id SERIAL PRIMARY KEY,
    producto_id INT NOT NULL,
    talle VARCHAR(20) NOT NULL,
    color VARCHAR(50) NOT NULL,
    stock INT DEFAULT 0 CHECK (stock >= 0),
    sku VARCHAR(100) UNIQUE NOT NULL,
    CONSTRAINT fk_producto FOREIGN KEY (producto_id) REFERENCES productos(id) ON DELETE CASCADE,
    CONSTRAINT unique_variante_producto UNIQUE (producto_id, talle, color)
);

-- 4. clientes (HU8)
CREATE TABLE clientes (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(150) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    direccion TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 5. cupones (HU4)
CREATE TABLE cupones (
    id SERIAL PRIMARY KEY,
    codigo VARCHAR(50) UNIQUE NOT NULL,
    porcentaje_descuento DECIMAL(5,2) NOT NULL CHECK (porcentaje_descuento BETWEEN 1 AND 100),
    fecha_vencimiento DATE NOT NULL,
    usos_maximos INT DEFAULT 1,
    usos_actuales INT DEFAULT 0
);

-- 6. carritos (HU11)
CREATE TABLE carritos (
    cliente_id INT PRIMARY KEY,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_cliente_carrito FOREIGN KEY (cliente_id) REFERENCES clientes(id) ON DELETE CASCADE
);

-- 7. carrito_items (HU11)
CREATE TABLE carrito_items (
    cliente_id INT NOT NULL,
    variante_id INT NOT NULL,
    cantidad INT NOT NULL CHECK (cantidad > 0),
    PRIMARY KEY (cliente_id, variante_id),
    CONSTRAINT fk_carrito_cliente FOREIGN KEY (cliente_id) REFERENCES carritos(cliente_id) ON DELETE CASCADE,
    CONSTRAINT fk_variante_carrito FOREIGN KEY (variante_id) REFERENCES variantes(id)
);

-- 8. compras (HU5, HU6, HU7)
CREATE TABLE compras (
    id SERIAL PRIMARY KEY,
    cliente_id INT NOT NULL,
    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    total DECIMAL(10,2) NOT NULL,
    estado VARCHAR(50) DEFAULT 'pendiente_pago' 
        CHECK (estado IN ('pendiente_pago', 'pagada', 'enviada', 'entregada', 'cancelada')),
    cupon_id INT,
    CONSTRAINT fk_cliente_compra FOREIGN KEY (cliente_id) REFERENCES clientes(id),
    CONSTRAINT fk_cupon_compra FOREIGN KEY (cupon_id) REFERENCES cupones(id) ON DELETE SET NULL
);

-- 9. compra_items (HU5)
CREATE TABLE compra_items (
    compra_id INT NOT NULL,
    variante_id INT NOT NULL,
    cantidad INT NOT NULL CHECK (cantidad > 0),
    precio_unitario DECIMAL(10,2) NOT NULL,
    PRIMARY KEY (compra_id, variante_id),
    CONSTRAINT fk_compra FOREIGN KEY (compra_id) REFERENCES compras(id) ON DELETE CASCADE,
    CONSTRAINT fk_variante_compra FOREIGN KEY (variante_id) REFERENCES variantes(id)
);