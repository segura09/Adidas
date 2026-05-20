import { createFileRoute } from "@tanstack/react-router";
import { AuthGuard } from "@/components/auth-guard";
import { AppShell } from "@/components/app-shell";

export const Route = createFileRoute("/_customer")({
  component: CustomerLayout,
});

const items = [
  { to: "/productos", label: "Productos" },
  { to: "/carrito", label: "Carrito" },
  { to: "/compras", label: "Mis compras" },
];

function CustomerLayout() {
  return (
    <AuthGuard>
      <AppShell title="Tienda" items={items} />
    </AuthGuard>
  );
}
