// HU10 — Stock bajo
// Endpoint backend:
//   GET /variantes/stock-bajo?umbral=5  -> LowStockVariant[]
import { createFileRoute } from "@tanstack/react-router";
import { useState } from "react";
import { useQuery } from "@tanstack/react-query";
import { api } from "@/lib/api";
import type { LowStockVariant } from "@/lib/types";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";

export const Route = createFileRoute("/admin/stock-bajo")({
  component: LowStockPage,
});

function LowStockPage() {
  const [umbral, setUmbral] = useState(5);
  const { data, isLoading } = useQuery({
    queryKey: ["stock-bajo", umbral],
    queryFn: () => api<LowStockVariant[]>(`/variantes/stock-bajo?umbral=${umbral}`),
  });

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-semibold">Variantes con stock bajo</h1>
      <Card>
        <CardHeader>
          <CardTitle>Filtro</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="flex max-w-xs items-end gap-3">
            <div className="flex-1 space-y-2">
              <Label>Umbral</Label>
              <Input
                type="number" min="0"
                value={umbral}
                onChange={(e) => setUmbral(Number(e.target.value))}
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
                  <TableHead>SKU</TableHead>
                  <TableHead>Producto</TableHead>
                  <TableHead>Talle</TableHead>
                  <TableHead>Color</TableHead>
                  <TableHead>Stock</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {data.map((v) => (
                  <TableRow key={v.id}>
                    <TableCell className="font-mono text-xs">{v.sku}</TableCell>
                    <TableCell>{v.producto_nombre ?? `#${v.producto_id}`}</TableCell>
                    <TableCell>{v.talle}</TableCell>
                    <TableCell>{v.color}</TableCell>
                    <TableCell>{v.stock}</TableCell>
                  </TableRow>
                ))}
                {data.length === 0 && (
                  <TableRow>
                    <TableCell colSpan={5} className="text-center text-muted-foreground">
                      Nada por debajo del umbral.
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
