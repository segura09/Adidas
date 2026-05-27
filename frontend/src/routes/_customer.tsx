import { createFileRoute } from "@tanstack/react-router";
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
  return <AppShell title="ADDIOS" items={items} />;
}
