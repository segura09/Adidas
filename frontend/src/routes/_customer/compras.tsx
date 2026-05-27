// HU8 — Historial de compras del cliente
// Endpoint backend:
//   GET /clientes/me/compras?estado=  -> Purchase[] ordenado por fecha desc
import { createFileRoute, Link, Outlet, useRouterState } from "@tanstack/react-router";
import { useState } from "react";
import { useQuery } from "@tanstack/react-query";
import { api } from "@/lib/api";
import type { Purchase, PurchaseStatus } from "@/lib/types";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { Label } from "@/components/ui/label";
import { Button } from "@/components/ui/button";
import { AuthGuard } from "@/components/auth-guard";

export const Route = createFileRoute("/_customer/compras")({
  component: ProtectedPurchasesPage,
});

const estados: (PurchaseStatus | "todos")[] = [
  "todos",
  "pendiente_pago",
  "pagada",
  "enviada",
  "entregada",
  "cancelada",
];

const estadoLabels: Record<PurchaseStatus | "todos", string> = {
  todos: "todos",
  pendiente_pago: "pendiente",
  pagada: "pagada",
  enviada: "enviada",
  entregada: "entregada",
  cancelada: "cancelada",
};

function ProtectedPurchasesPage() {
  return (
    <AuthGuard>
      <PurchasesPage />
    </AuthGuard>
  );
}

function PurchasesPage() {
  const isChildRoute = useRouterState({
    select: (state) => state.location.pathname !== "/compras",
  });
  const [estado, setEstado] = useState<string>("todos");

  const qs = estado !== "todos" ? `?estado=${estado}` : "";
  const { data, isLoading } = useQuery({
    queryKey: ["compras", estado],
    queryFn: () => api<Purchase[]>(`/clientes/me/compras${qs}`),
  });

  if (isChildRoute) {
    return <Outlet />;
  }

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-semibold">Mis compras</h1>

      <Card>
        <CardContent className="pt-6">
          <div className="flex max-w-xs flex-col gap-2">
            <Label>Filtrar por estado</Label>
            <Select value={estado} onValueChange={setEstado}>
              <SelectTrigger>
                <SelectValue />
              </SelectTrigger>
              <SelectContent>
                {estados.map((s) => (
                  <SelectItem key={s} value={s}>
                    {estadoLabels[s]}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>
        </CardContent>
      </Card>

      {isLoading && <p className="text-sm text-muted-foreground">Cargando…</p>}
      {data && (
        <div className="space-y-3">
          {data.map((p) => (
            <Card key={p.id}>
              <CardHeader className="flex-row items-center justify-between gap-2">
                <div>
                  <CardTitle className="text-base">Compra #{p.id}</CardTitle>
                  <p className="text-xs text-muted-foreground">
                    {new Date(p.fecha).toLocaleString()}
                  </p>
                </div>
                <Badge variant="secondary">{estadoLabels[p.estado]}</Badge>
              </CardHeader>
              <CardContent className="flex items-center justify-between">
                <span className="text-lg font-semibold">${p.total.toFixed(2)}</span>
                <Button asChild size="sm" variant="outline">
                  <Link to="/compras/$id" params={{ id: String(p.id) }}>
                    Ver detalle
                  </Link>
                </Button>
              </CardContent>
            </Card>
          ))}
          {data.length === 0 && (
            <p className="text-center text-sm text-muted-foreground">Sin compras todavía.</p>
          )}
        </div>
      )}
    </div>
  );
}
