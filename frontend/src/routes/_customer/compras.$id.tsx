// HU7 — Detalle de compra con transiciones de estado
// Endpoints backend:
//   GET  /compras/{id}                 -> Purchase
//   POST /compras/{id}/pagar           -> Purchase   (marca pagada y descuenta stock)
//   POST /compras/{id}/cancelar        -> Purchase   (restaura stock si correspondía)
//   POST /compras/{id}/enviar          -> Purchase
//   POST /compras/{id}/entregar        -> Purchase
import { createFileRoute, useParams, Link } from "@tanstack/react-router";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { api } from "@/lib/api";
import type { Purchase } from "@/lib/types";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";

export const Route = createFileRoute("/_customer/compras/$id")({
  component: PurchaseDetailPage,
});

function PurchaseDetailPage() {
  const { id } = useParams({ from: "/_customer/compras/$id" });
  const qc = useQueryClient();

  const { data, isLoading } = useQuery({
    queryKey: ["compra", id],
    queryFn: () => api<Purchase>(`/compras/${id}`),
  });

  function action(path: string) {
    return useMutation({
      mutationFn: () => api<Purchase>(`/compras/${id}/${path}`, { method: "POST" }),
      onSuccess: () => qc.invalidateQueries({ queryKey: ["compra", id] }),
    });
  }

  // hooks must be called unconditionally
  const pagar = action("pagar");
  const cancelar = action("cancelar");
  const enviar = action("enviar");
  const entregar = action("entregar");

  if (isLoading || !data) {
    return <p className="text-sm text-muted-foreground">Cargando…</p>;
  }

  const allowed = (estado: string) => {
    switch (data.estado) {
      case "pendiente":
        return ["pagar", "cancelar"].includes(estado);
      case "pagada":
        return ["enviar", "cancelar"].includes(estado);
      case "enviada":
        return ["entregar"].includes(estado);
      default:
        return false;
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-semibold">Compra #{data.id}</h1>
        <Badge variant="secondary">{data.estado}</Badge>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Items</CardTitle>
        </CardHeader>
        <CardContent className="overflow-x-auto">
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>Producto</TableHead>
                <TableHead>Variante</TableHead>
                <TableHead>Cantidad</TableHead>
                <TableHead>P. Unitario</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {data.items.map((it, i) => (
                <TableRow key={i}>
                  <TableCell>{it.producto_nombre ?? `Var #${it.variante_id}`}</TableCell>
                  <TableCell>
                    {it.talle} · {it.color}
                  </TableCell>
                  <TableCell>{it.cantidad}</TableCell>
                  <TableCell>${it.precio_unitario.toFixed(2)}</TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
          <div className="mt-4 flex justify-end gap-6 text-sm">
            {data.descuento ? (
              <span className="text-muted-foreground">
                Descuento: -${data.descuento.toFixed(2)}
              </span>
            ) : null}
            <span className="text-lg font-semibold">Total: ${data.total.toFixed(2)}</span>
          </div>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>Acciones</CardTitle>
        </CardHeader>
        <CardContent className="flex flex-wrap gap-2">
          {allowed("pagar") && (
            <Button onClick={() => pagar.mutate()} disabled={pagar.isPending}>
              Marcar pagada
            </Button>
          )}
          {allowed("enviar") && (
            <Button onClick={() => enviar.mutate()} disabled={enviar.isPending}>
              Marcar enviada
            </Button>
          )}
          {allowed("entregar") && (
            <Button onClick={() => entregar.mutate()} disabled={entregar.isPending}>
              Marcar entregada
            </Button>
          )}
          {allowed("cancelar") && (
            <Button
              variant="destructive"
              onClick={() => cancelar.mutate()}
              disabled={cancelar.isPending}
            >
              Cancelar
            </Button>
          )}
          {data.estado === "entregada" && (
            <Button asChild variant="outline">
              <Link to="/compras/$id/devolucion" params={{ id }}>
                Solicitar devolución
              </Link>
            </Button>
          )}
          {!allowed("pagar") &&
            !allowed("enviar") &&
            !allowed("entregar") &&
            !allowed("cancelar") &&
            data.estado !== "entregada" && (
              <p className="text-sm text-muted-foreground">No hay acciones disponibles.</p>
            )}
        </CardContent>
      </Card>
    </div>
  );
}
