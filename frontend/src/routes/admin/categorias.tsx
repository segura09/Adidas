// HU1 — Alta de categorías
// Endpoints backend:
//   GET    /categorias          -> Category[]
//   POST   /categorias          -> Category   body: { nombre }
import { createFileRoute } from "@tanstack/react-router";
import { useState, type FormEvent } from "react";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { api } from "@/lib/api";
import type { Category } from "@/lib/types";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";

export const Route = createFileRoute("/admin/categorias")({
  component: CategoriesPage,
});

function CategoriesPage() {
  const qc = useQueryClient();
  const [nombre, setNombre] = useState("");

  const { data, isLoading, error } = useQuery({
    queryKey: ["categorias"],
    queryFn: () => api<Category[]>("/categorias"),
  });

  const create = useMutation({
    mutationFn: (nombre: string) =>
      api<Category>("/categorias", { method: "POST", body: { nombre } }),
    onSuccess: () => {
      setNombre("");
      qc.invalidateQueries({ queryKey: ["categorias"] });
    },
  });

  function onSubmit(e: FormEvent) {
    e.preventDefault();
    if (!nombre.trim()) return;
    create.mutate(nombre.trim());
  }

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-semibold">Categorías</h1>

      <Card>
        <CardHeader>
          <CardTitle>Nueva categoría</CardTitle>
          <CardDescription>El nombre debe ser único.</CardDescription>
        </CardHeader>
        <CardContent>
          <form onSubmit={onSubmit} className="flex flex-col gap-3 sm:flex-row sm:items-end">
            <div className="flex-1 space-y-2">
              <Label htmlFor="nombre">Nombre</Label>
              <Input id="nombre" value={nombre} onChange={(e) => setNombre(e.target.value)} required />
            </div>
            <Button type="submit" disabled={create.isPending}>
              {create.isPending ? "Creando…" : "Crear"}
            </Button>
          </form>
          {create.error && (
            <p className="mt-2 text-sm text-destructive">{(create.error as Error).message}</p>
          )}
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>Listado</CardTitle>
        </CardHeader>
        <CardContent>
          {isLoading && <p className="text-sm text-muted-foreground">Cargando…</p>}
          {error && <p className="text-sm text-destructive">{(error as Error).message}</p>}
          {data && (
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead className="w-20">ID</TableHead>
                  <TableHead>Nombre</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {data.map((c) => (
                  <TableRow key={c.id}>
                    <TableCell>{c.id}</TableCell>
                    <TableCell>{c.nombre}</TableCell>
                  </TableRow>
                ))}
                {data.length === 0 && (
                  <TableRow>
                    <TableCell colSpan={2} className="text-center text-muted-foreground">
                      Sin categorías todavía.
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
