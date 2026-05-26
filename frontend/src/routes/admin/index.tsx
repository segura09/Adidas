import { createFileRoute, Link } from "@tanstack/react-router";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

export const Route = createFileRoute("/admin/")({
  component: AdminHome,
});

const tiles = [
  { to: "/admin/categorias", title: "Categorías", desc: "Crear y listar categorías." },
  { to: "/admin/productos", title: "Productos", desc: "ABM de productos y variantes." },
  { to: "/admin/compras", title: "Compras", desc: "Confirmar pagos y gestionar estados." },
  { to: "/admin/cupones", title: "Cupones", desc: "Gestionar cupones de descuento." },
  { to: "/admin/stock-bajo", title: "Stock bajo", desc: "Variantes por debajo del umbral." },
  { to: "/admin/reportes/top-productos", title: "Top productos", desc: "Más vendidos." },
  { to: "/admin/reportes/facturacion", title: "Facturación", desc: "Reporte por período." },
];

function AdminHome() {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-semibold">Panel de administración</h1>
        <p className="text-sm text-muted-foreground">Accesos rápidos a la gestión.</p>
      </div>
      <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">
        {tiles.map((t) => (
          <Link key={t.to} to={t.to}>
            <Card className="h-full transition-colors hover:bg-accent">
              <CardHeader>
                <CardTitle className="text-base">{t.title}</CardTitle>
              </CardHeader>
              <CardContent className="text-sm text-muted-foreground">{t.desc}</CardContent>
            </Card>
          </Link>
        ))}
      </div>
    </div>
  );
}
