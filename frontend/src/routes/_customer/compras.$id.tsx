// HU7 — Detalle de compra con transiciones de estado
// Endpoints backend:
//   GET  /compras/{id}                 -> Purchase
//   POST /compras/{id}/pagar           -> Purchase   (marca pagada y descuenta stock)
//   POST /compras/{id}/cancelar        -> Purchase   (restaura stock si correspondía)
//   POST /compras/{id}/enviar          -> Purchase
//   POST /compras/{id}/entregar        -> Purchase
import { createFileRoute, useParams, Link } from "@tanstack/react-router";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { useState, type FormEvent } from "react";
import { api } from "@/lib/api";
import type { Purchase } from "@/lib/types";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { AuthGuard } from "@/components/auth-guard";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";

export const Route = createFileRoute("/_customer/compras/$id")({
  component: ProtectedPurchaseDetailPage,
});

function ProtectedPurchaseDetailPage() {
  return (
    <AuthGuard>
      <PurchaseDetailPage />
    </AuthGuard>
  );
}

function PurchaseDetailPage() {
  const { id } = useParams({ from: "/_customer/compras/$id" });
  const qc = useQueryClient();
  const [reviewProduct, setReviewProduct] = useState<{ id: number; nombre: string } | null>(null);
  const [puntaje, setPuntaje] = useState(5);
  const [comentario, setComentario] = useState("");

  const { data, isLoading } = useQuery({
    queryKey: ["compra", id],
    queryFn: () => api<Purchase>(`/compras/${id}`),
  });

  function action(path: string) {
    return useMutation({
      mutationFn: () => api<Purchase>(`/compras/${id}/${path}`, { method: "POST" }),
      onSuccess: () => {
        qc.invalidateQueries({ queryKey: ["compra", id] });
        qc.invalidateQueries({ queryKey: ["compras"] });
      },
    });
  }

  // hooks must be called unconditionally
  const cancelar = action("cancelar");
  const createReview = useMutation({
    mutationFn: () =>
      api(`/productos/${reviewProduct?.id}/resenas`, {
        method: "POST",
        body: {
          puntaje,
          comentario: comentario.trim() || undefined,
        },
      }),
    onSuccess: () => {
      if (reviewProduct) {
        qc.invalidateQueries({ queryKey: ["resenas", String(reviewProduct.id)] });
        qc.invalidateQueries({ queryKey: ["resenas-resumen", String(reviewProduct.id)] });
      }
      setReviewProduct(null);
      setPuntaje(5);
      setComentario("");
    },
  });

  if (isLoading || !data) {
    return <p className="text-sm text-muted-foreground">Cargando…</p>;
  }

  const canCancel = data.estado === "pendiente_pago";
  const renderedReviewProducts = new Set<number>();

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-semibold">Compra #{data.id}</h1>
        <Badge variant="secondary">{data.estado === "pendiente_pago" ? "pendiente" : data.estado}</Badge>
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
                {data.estado === "entregada" && <TableHead></TableHead>}
              </TableRow>
            </TableHeader>
            <TableBody>
              {data.items.map((it, i) => {
                const canReviewThisProduct =
                  data.estado === "entregada" &&
                  !!it.producto_id &&
                  !renderedReviewProducts.has(it.producto_id);
                if (it.producto_id) renderedReviewProducts.add(it.producto_id);

                return (
                <TableRow key={i}>
                  <TableCell>{it.producto_nombre ?? `Var #${it.variante_id}`}</TableCell>
                  <TableCell>
                    {it.talle} · {it.color}
                  </TableCell>
                  <TableCell>{it.cantidad}</TableCell>
                  <TableCell>${it.precio_unitario.toFixed(2)}</TableCell>
                  {data.estado === "entregada" && (
                    <TableCell className="text-right">
                      {canReviewThisProduct && (
                        <Button
                          size="sm"
                          variant="outline"
                          onClick={() =>
                            setReviewProduct({
                              id: it.producto_id!,
                              nombre: it.producto_nombre ?? `Producto #${it.producto_id}`,
                            })
                          }
                        >
                          Reseñar
                        </Button>
                      )}
                    </TableCell>
                  )}
                </TableRow>
                );
              })}
            </TableBody>
          </Table>
          <div className="mt-4 space-y-2 text-right text-sm">
            <p className="text-muted-foreground">
              Subtotal: ${(data.subtotal ?? data.total + (data.descuento ?? 0)).toFixed(2)}
            </p>
            <p className="text-muted-foreground">
              Descuento: {data.descuento ? `-$${data.descuento.toFixed(2)}` : "sin descuento"}
            </p>
            <p className="text-lg font-semibold">Total: ${data.total.toFixed(2)}</p>
          </div>
        </CardContent>
      </Card>

      {reviewProduct && (
        <Card>
          <CardHeader>
            <CardTitle>Reseñar {reviewProduct.nombre}</CardTitle>
          </CardHeader>
          <CardContent>
            <form
              onSubmit={(e: FormEvent) => {
                e.preventDefault();
                createReview.mutate();
              }}
              className="space-y-3"
            >
              <div className="space-y-2">
                <Label>Puntaje</Label>
                <Select value={String(puntaje)} onValueChange={(v) => setPuntaje(Number(v))}>
                  <SelectTrigger className="w-32">
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    {[1, 2, 3, 4, 5].map((n) => (
                      <SelectItem key={n} value={String(n)}>
                        {n} estrellas
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>
              <div className="space-y-2">
                <Label>Comentario opcional</Label>
                <Textarea value={comentario} onChange={(e) => setComentario(e.target.value)} />
              </div>
              <div className="flex flex-wrap gap-2">
                <Button type="submit" disabled={createReview.isPending}>
                  {createReview.isPending ? "Enviando..." : "Enviar reseña"}
                </Button>
                <Button type="button" variant="outline" onClick={() => setReviewProduct(null)}>
                  Cancelar
                </Button>
              </div>
              {createReview.error && (
                <p className="text-sm text-destructive">{(createReview.error as Error).message}</p>
              )}
            </form>
          </CardContent>
        </Card>
      )}

      <Card>
        <CardHeader>
          <CardTitle>Acciones</CardTitle>
        </CardHeader>
        <CardContent className="flex flex-wrap gap-2">
          {canCancel && (
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
          {!canCancel && data.estado !== "entregada" && (
            <p className="text-sm text-muted-foreground">No hay acciones disponibles.</p>
          )}
        </CardContent>
      </Card>
    </div>
  );
}
