// HU9 — Productos más vendidos
// Endpoint backend:
//   GET /productos/top?limit=10  -> TopProduct[]
import { createFileRoute } from "@tanstack/react-router";
import { useState } from "react";
import { useQuery } from "@tanstack/react-query";
import { api } from "@/lib/api";
import type { TopProduct } from "@/lib/types";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";

export const Route = createFileRoute("/admin/reportes/top-productos")({
  component: TopProductsPage,
});

function TopProductsPage() {
  const [limit, setLimit] = useState(10);
  const { data, isLoading } = useQuery({
    queryKey: ["top-productos", limit],
    queryFn: () => api<TopProduct[]>(`/productos/top?limit=${limit}`),
  });

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-semibold">Productos más vendidos</h1>
      <Card>
        <CardHeader>
          <CardTitle>Filtro</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="flex max-w-xs items-end gap-3">
            <div className="flex-1 space-y-2">
              <Label>Top</Label>
              <Input
                type="number" min="1"
                value={limit}
                onChange={(e) => setLimit(Number(e.target.value))}
              />
            </div>
          </div>
        </CardContent>
      </Card>

      <Card>
        <CardContent className="overflow-x-auto pt-6">
          {isLoading && <p className="text-sm text-muted-foreground">Cargando…</p>}
          {data && (
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead className="w-16">#</TableHead>
                  <TableHead>Producto</TableHead>
                  <TableHead>Unidades</TableHead>
                  <TableHead>Facturación</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {data.map((p, i) => (
                  <TableRow key={p.producto_id}>
                    <TableCell>{i + 1}</TableCell>
                    <TableCell>{p.nombre}</TableCell>
                    <TableCell>{p.unidades_vendidas}</TableCell>
                    <TableCell>${p.facturacion.toFixed(2)}</TableCell>
                  </TableRow>
                ))}
                {data.length === 0 && (
                  <TableRow>
                    <TableCell colSpan={4} className="text-center text-muted-foreground">
                      Aún no hay datos.
                    </TableCell>
                  </TableRow>
                )}
              </TableBody>
            </Table>
          )}
        </CardContent>
      </Card>
    </div>
  );
}
