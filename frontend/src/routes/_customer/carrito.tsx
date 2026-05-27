// HU11 — Carrito persistente
// Endpoints backend:
//   GET    /carritos/me          -> Cart
//   DELETE /carritos/items/{varianteId}  -> Cart
//   DELETE /carritos/me          -> 204 (vaciar)
import { createFileRoute, Link } from "@tanstack/react-router";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { api } from "@/lib/api";
import type { Cart } from "@/lib/types";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { AuthGuard } from "@/components/auth-guard";

export const Route = createFileRoute("/_customer/carrito")({
  component: ProtectedCartPage,
});

function ProtectedCartPage() {
  return (
    <AuthGuard>
      <CartPage />
    </AuthGuard>
  );
}

function CartPage() {
  const qc = useQueryClient();
  const { data, isLoading } = useQuery({
    queryKey: ["carrito"],
    queryFn: () => api<Cart>("/carritos/me"),
  });

  const removeItem = useMutation({
    mutationFn: (varianteId: number) =>
      api(`/carritos/items/${varianteId}`, { method: "DELETE" }),
    onSuccess: () => qc.invalidateQueries({ queryKey: ["carrito"] }),
  });

  const clearCart = useMutation({
    mutationFn: () => api("/carritos/me", { method: "DELETE" }),
    onSuccess: () => qc.invalidateQueries({ queryKey: ["carrito"] }),
  });

  const subtotal =
    data?.items.reduce((acc, it) => acc + (it.precio_unitario ?? 0) * it.cantidad, 0) ?? 0;

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-semibold">Mi carrito</h1>
      {isLoading && <p className="text-sm text-muted-foreground">Cargando…</p>}
      {data && (
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
                  <TableHead>Precio</TableHead>
                  <TableHead></TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {data.items.map((it) => (
                  <TableRow key={it.variante_id}>
                    <TableCell>{it.producto_nombre ?? `Var #${it.variante_id}`}</TableCell>
                    <TableCell>
                      {it.talle} · {it.color}
                    </TableCell>
                    <TableCell>{it.cantidad}</TableCell>
                    <TableCell>${(it.precio_unitario ?? 0).toFixed(2)}</TableCell>
                    <TableCell className="text-right">
                      <Button
                        size="sm"
                        variant="ghost"
                        onClick={() => removeItem.mutate(it.variante_id)}
                      >
                        Quitar
                      </Button>
                    </TableCell>
                  </TableRow>
                ))}
                {data.items.length === 0 && (
                  <TableRow>
                    <TableCell colSpan={5} className="text-center text-muted-foreground">
                      Tu carrito está vacío.
                    </TableCell>
                  </TableRow>
                )}
              </TableBody>
            </Table>

            {data.items.length > 0 && (
              <div className="mt-4 flex flex-col items-end gap-3 sm:flex-row sm:items-center sm:justify-between">
                <Button variant="outline" onClick={() => clearCart.mutate()}>
                  Vaciar carrito
                </Button>
                <div className="flex items-center gap-4">
                  <span className="text-sm text-muted-foreground">Subtotal:</span>
                  <span className="text-lg font-semibold">${subtotal.toFixed(2)}</span>
                  <Button asChild>
                    <Link to="/checkout">Ir al checkout</Link>
                  </Button>
                </div>
              </div>
            )}
          </CardContent>
        </Card>
      )}
    </div>
  );
}
