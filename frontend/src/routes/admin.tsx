import { createFileRoute } from "@tanstack/react-router";
import { AuthGuard } from "@/components/auth-guard";
import { AppShell } from "@/components/app-shell";

export const Route = createFileRoute("/admin")({
  component: AdminLayout,
});

const items = [
  { to: "/admin", label: "Inicio" },
  { to: "/admin/categorias", label: "Categorías" },
  { to: "/admin/productos", label: "Productos" },
  { to: "/admin/cupones", label: "Cupones" },
  { to: "/admin/stock-bajo", label: "Stock bajo" },
  { to: "/admin/reportes/top-productos", label: "Top productos" },
  { to: "/admin/reportes/facturacion", label: "Facturación" },
];

function AdminLayout() {
  return (
    <AuthGuard requireAdmin>
      <AppShell title="Admin" items={items} />
    </AuthGuard>
  );
}
