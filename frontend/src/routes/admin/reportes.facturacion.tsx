// HU14 — Reporte de facturación
// Endpoint backend:
//   GET /reportes/facturacion?desde=YYYY-MM-DD&hasta=YYYY-MM-DD -> BillingReport
import { createFileRoute } from "@tanstack/react-router";
import { useState } from "react";
import { useQuery } from "@tanstack/react-query";
import { api } from "@/lib/api";
import type { BillingReport } from "@/lib/types";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Button } from "@/components/ui/button";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";

export const Route = createFileRoute("/admin/reportes/facturacion")({
  component: BillingReportPage,
});

function BillingReportPage() {
  const today = new Date().toISOString().slice(0, 10);
  const monthAgo = new Date(Date.now() - 30 * 86400000).toISOString().slice(0, 10);
  const [desde, setDesde] = useState(monthAgo);
  const [hasta, setHasta] = useState(today);
  const [enabled, setEnabled] = useState(true);

  const { data, isLoading, refetch } = useQuery({
    queryKey: ["facturacion", desde, hasta],
    queryFn: () =>
      api<BillingReport>(`/reportes/facturacion?desde=${desde}&hasta=${hasta}`),
    enabled,
  });

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-semibold">Reporte de facturación</h1>
      <Card>
        <CardHeader>
          <CardTitle>Período</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 items-end gap-3 sm:grid-cols-3">
            <div className="space-y-2">
              <Label>Desde</Label>
              <Input type="date" value={desde} onChange={(e) => setDesde(e.target.value)} />
            </div>
            <div className="space-y-2">
              <Label>Hasta</Label>
              <Input type="date" value={hasta} onChange={(e) => setHasta(e.target.value)} />
            </div>
            <Button
              onClick={() => {
                setEnabled(true);
                refetch();
              }}
            >
              Generar
            </Button>
          </div>
        </CardContent>
      </Card>

      {isLoading && <p className="text-sm text-muted-foreground">Cargando…</p>}
      {data && (
        <div className="grid gap-4 md:grid-cols-3">
          <Card>
            <CardHeader>
              <CardTitle className="text-base">Total facturado</CardTitle>
            </CardHeader>
            <CardContent className="text-3xl font-semibold">
              ${data.total_facturado.toFixed(2)}
            </CardContent>
          </Card>
          <Card>
            <CardHeader>
              <CardTitle className="text-base">Compras</CardTitle>
            </CardHeader>
            <CardContent className="text-3xl font-semibold">{data.cantidad_compras}</CardContent>
          </Card>
          <Card>
            <CardHeader>
              <CardTitle className="text-base">Período</CardTitle>
            </CardHeader>
            <CardContent className="text-sm text-muted-foreground">
              {data.desde} → {data.hasta}
            </CardContent>
          </Card>
        </div>
      )}

      {data && (
        <Card>
          <CardHeader>
            <CardTitle>Por categoría</CardTitle>
          </CardHeader>
          <CardContent className="overflow-x-auto">
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>Categoría</TableHead>
                  <TableHead className="text-right">Total</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {data.por_categoria.map((c) => (
                  <TableRow key={c.categoria_id}>
                    <TableCell>{c.nombre}</TableCell>
                    <TableCell className="text-right">${c.total.toFixed(2)}</TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </CardContent>
        </Card>
      )}
    </div>
  );
}
