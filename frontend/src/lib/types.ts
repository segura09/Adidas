// Tipos compartidos con el backend FastAPI.
// Ajustar si los DTOs reales cambian.

export interface User {
  id: number;
  email: string;
  nombre?: string;
  isAdmin: boolean;
}

export interface AuthResponse {
  access_token: string;
  token_type: string;
  user: User;
}

export interface Category {
  id: number;
  nombre: string;
}

export interface Product {
  id: number;
  nombre: string;
  descripcion?: string;
  precio_base: number;
  categoria_id: number;
  activo: boolean;
}

export interface Variant {
  id: number;
  producto_id: number;
  talle: string;
  color: string;
  stock: number;
  sku: string;
}

export interface Coupon {
  id: number;
  codigo: string;
  porcentaje_descuento: number;
  fecha_vencimiento: string;
  usos_maximos: number;
  usos_actuales: number;
}

export interface CartItem {
  variante_id: number;
  cantidad: number;
  // metadatos opcionales que devuelve el backend
  producto_nombre?: string;
  talle?: string;
  color?: string;
  precio_unitario?: number;
}

export interface Cart {
  id: number;
  cliente_id: number;
  items: CartItem[];
}

export type PurchaseStatus =
  | "pendiente_pago"
  | "pagada"
  | "enviada"
  | "entregada"
  | "cancelada";

export interface PurchaseItem {
  variante_id: number;
  cantidad: number;
  precio_unitario: number;
  producto_nombre?: string;
  talle?: string;
  color?: string;
}

export interface Purchase {
  id: number;
  cliente_id: number;
  fecha: string;
  estado: PurchaseStatus;
  total: number;
  subtotal?: number;
  descuento?: number;
  cupon_id?: number | null;
  items: PurchaseItem[];
}

export interface Review {
  id: number;
  cliente_id: number;
  producto_id: number;
  puntaje: number;
  comentario?: string;
  fecha: string;
}

export interface ReviewSummary {
  promedio: number;
  cantidad: number;
}

export interface ReturnItem {
  variante_id: number;
  cantidad: number;
}

export interface Return {
  id: number;
  compra_id: number;
  estado: "solicitada" | "aprobada" | "rechazada" | "reintegrada";
  items: ReturnItem[];
  motivo?: string;
}

export interface TopProduct {
  producto_id: number;
  nombre: string;
  unidades_vendidas: number;
  facturacion: number;
}

export interface LowStockVariant extends Variant {
  producto_nombre?: string;
}

export interface BillingReport {
  desde: string;
  hasta: string;
  total_facturado: number;
  cantidad_compras: number;
  por_categoria: { categoria_id: number; nombre: string; total: number }[];
}
