// HU2 — Variantes de producto
// Endpoints backend:
//   GET  /productos/{id}/variantes        -> Variant[]
//   POST /productos/{id}/variantes        -> Variant  body: { talle, color, stock, sku }
//   PUT  /variantes/{varianteId}/stock    -> Variant  body: { stock }
import { createFileRoute, useParams, Link } from "@tanstack/react-router";
import { useState, type FormEvent } from "react";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { api } from "@/lib/api";
import type { Variant } from "@/lib/types";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";

export const Route = createFileRoute("/admin/productos/$id/variantes")({
  component: VariantsPage,
});

interface FormState {
  talle: string;
  color: string;
  stock: string;
}
const empty: FormState = { talle: "", color: "", stock: "0" };

function VariantsPage() {
  const { id } = useParams({ from: "/admin/productos/$id/variantes" });
  const qc = useQueryClient();
  const [form, setForm] = useState<FormState>(empty);

  const { data, isLoading } = useQuery({
    queryKey: ["variantes", id],
    queryFn: () => api<Variant[]>(`/productos/${id}/variantes`),
  });

  const create = useMutation({
    mutationFn: (f: FormState) =>
      api<Variant>(`/productos/${id}/variantes`, {
        method: "POST",
        body: {
          talle: f.talle,
          color: f.color,
          stock: Number(f.stock),
          sku: buildSku(id, f.talle, f.color),
        },
      }),
    onSuccess: () => {
      setForm(empty);
      qc.invalidateQueries({ queryKey: ["variantes", id] });
    },
  });

  const updateStock = useMutation({
    mutationFn: ({ varianteId, stock }: { varianteId: number; stock: number }) =>
      api(`/variantes/${varianteId}/stock`, { method: "PUT", body: { stock } }),
    onSuccess: () => qc.invalidateQueries({ queryKey: ["variantes", id] }),
  });

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-semibold">Variantes del producto #{id}</h1>
        <Button asChild variant="outline">
          <Link to="/admin/productos">Volver</Link>
        </Button>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Nueva variante</CardTitle>
        </CardHeader>
        <CardContent>
          <form
            onSubmit={(e: FormEvent) => {
              e.preventDefault();
              create.mutate(form);
            }}
            className="grid grid-cols-1 gap-3 md:grid-cols-3"
          >
            <div className="space-y-2">
              <Label>Talle</Label>
              <Input value={form.talle} onChange={(e) => setForm({ ...form, talle: e.target.value })} required />
            </div>
            <div className="space-y-2">
              <Label>Color</Label>
              <Input value={form.color} onChange={(e) => setForm({ ...form, color: e.target.value })} required />
            </div>
            <div className="space-y-2">
              <Label>Stock</Label>
              <Input
                type="number"
                min="0"
                value={form.stock}
                onChange={(e) => setForm({ ...form, stock: e.target.value })}
                required
              />
            </div>
            <div className="md:col-span-3">
              <Button type="submit" disabled={create.isPending}>
                {create.isPending ? "Creando…" : "Crear variante"}
              </Button>
              {create.error && (
                <span className="ml-3 text-sm text-destructive">{(create.error as Error).message}</span>
              )}
            </div>
          </form>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>Listado</CardTitle>
        </CardHeader>
        <CardContent className="overflow-x-auto">
          {isLoading && <p className="text-sm text-muted-foreground">Cargando…</p>}
          {data && (
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>SKU</TableHead>
                  <TableHead>Talle</TableHead>
                  <TableHead>Color</TableHead>
                  <TableHead>Stock</TableHead>
                  <TableHead className="text-right">Acciones</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {data.map((v) => (
                  <TableRow key={v.id}>
                    <TableCell className="font-mono text-xs">{v.sku}</TableCell>
                    <TableCell>{v.talle}</TableCell>
                    <TableCell>{v.color}</TableCell>
                    <TableCell>{v.stock}</TableCell>
                    <TableCell className="text-right">
                      <Button
                        size="sm"
                        variant="outline"
                        onClick={() => {
                          const val = window.prompt("Nuevo stock", String(v.stock));
                          if (val !== null) updateStock.mutate({ varianteId: v.id, stock: Number(val) });
                        }}
                      >
                        Editar stock
                      </Button>
                    </TableCell>
                  </TableRow>
                ))}
                {data.length === 0 && (
                  <TableRow>
                    <TableCell colSpan={5} className="text-center text-muted-foreground">
                      Sin variantes cargadas.
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

function buildSku(productId: string, talle: string, color: string) {
  const base = `PROD-${productId}-${talle}-${color}`
    .toUpperCase()
    .replace(/[^A-Z0-9]+/g, "-")
    .replace(/^-|-$/g, "")
    .slice(0, 40);

  return `${base}-${Date.now().toString().slice(-6)}`;
}
