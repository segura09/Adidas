// HU4 — Cupones de descuento
// Endpoints backend:
//   GET  /cupones        -> Coupon[]
//   POST /cupones        -> Coupon  body: { codigo, porcentaje_descuento, fecha_vencimiento, usos_maximos }
import { createFileRoute } from "@tanstack/react-router";
import { useState, type FormEvent } from "react";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { api } from "@/lib/api";
import type { Coupon } from "@/lib/types";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";

export const Route = createFileRoute("/admin/cupones")({
  component: CouponsPage,
});

interface FormState {
  codigo: string;
  porcentaje_descuento: string;
  fecha_vencimiento: string;
  usos_maximos: string;
}
const empty: FormState = { codigo: "", porcentaje_descuento: "10", fecha_vencimiento: "", usos_maximos: "100" };

function CouponsPage() {
  const qc = useQueryClient();
  const [form, setForm] = useState<FormState>(empty);

  const { data, isLoading } = useQuery({
    queryKey: ["cupones"],
    queryFn: () => api<Coupon[]>("/cupones"),
  });

  const create = useMutation({
    mutationFn: (f: FormState) =>
      api<Coupon>("/cupones", {
        method: "POST",
        body: {
          codigo: f.codigo,
          porcentaje_descuento: Number(f.porcentaje_descuento),
          fecha_vencimiento: f.fecha_vencimiento,
          usos_maximos: Number(f.usos_maximos),
        },
      }),
    onSuccess: () => {
      setForm(empty);
      qc.invalidateQueries({ queryKey: ["cupones"] });
    },
  });

  const remove = useMutation({
    mutationFn: (id: number) => api(`/cupones/${id}`, { method: "DELETE" }),
    onSuccess: () => qc.invalidateQueries({ queryKey: ["cupones"] }),
  });

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-semibold">Cupones</h1>

      <Card>
        <CardHeader>
          <CardTitle>Nuevo cupón</CardTitle>
        </CardHeader>
        <CardContent>
          <form
            onSubmit={(e: FormEvent) => {
              e.preventDefault();
              create.mutate(form);
            }}
            className="grid grid-cols-1 gap-3 md:grid-cols-4"
          >
            <div className="space-y-2">
              <Label>Código</Label>
              <Input value={form.codigo} onChange={(e) => setForm({ ...form, codigo: e.target.value })} required />
            </div>
            <div className="space-y-2">
              <Label>Descuento %</Label>
              <Input
                type="number" min="1" max="100"
                value={form.porcentaje_descuento}
                onChange={(e) => setForm({ ...form, porcentaje_descuento: e.target.value })}
                required
              />
            </div>
            <div className="space-y-2">
              <Label>Vencimiento</Label>
              <Input
                type="date"
                value={form.fecha_vencimiento}
                onChange={(e) => setForm({ ...form, fecha_vencimiento: e.target.value })}
                required
              />
            </div>
            <div className="space-y-2">
              <Label>Usos máximos</Label>
              <Input
                type="number" min="1"
                value={form.usos_maximos}
                onChange={(e) => setForm({ ...form, usos_maximos: e.target.value })}
                required
              />
            </div>
            <div className="md:col-span-4">
              <Button type="submit" disabled={create.isPending}>
                {create.isPending ? "Creando…" : "Crear cupón"}
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
                  <TableHead>Código</TableHead>
                  <TableHead>%</TableHead>
                  <TableHead>Vence</TableHead>
                  <TableHead>Usos</TableHead>
                  <TableHead className="text-right">Acciones</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {data.map((c) => (
                  <TableRow key={c.id}>
                    <TableCell className="font-mono">{c.codigo}</TableCell>
                    <TableCell>{c.porcentaje_descuento}%</TableCell>
                    <TableCell>{c.fecha_vencimiento}</TableCell>
                    <TableCell>
                      {c.usos_actuales} / {c.usos_maximos}
                    </TableCell>
                    <TableCell className="text-right">
                      <Button
                        size="sm"
                        variant="destructive"
                        disabled={remove.isPending}
                        onClick={() => {
                          if (window.confirm(`Eliminar cupón ${c.codigo}?`)) {
                            remove.mutate(c.id);
                          }
                        }}
                      >
                        Eliminar
                      </Button>
                    </TableCell>
                  </TableRow>
                ))}
                {data.length === 0 && (
                  <TableRow>
                    <TableCell colSpan={5} className="text-center text-muted-foreground">
                      Sin cupones.
                    </TableCell>
                  </TableRow>
                )}
              </TableBody>
            </Table>
          )}
          {remove.error && (
            <p className="mt-3 text-sm text-destructive">{(remove.error as Error).message}</p>
          )}
        </CardContent>
      </Card>
    </div>
  );
}
