// HU3 — Buscar productos (cliente)
// Endpoints backend:
//   GET /categorias                                              -> Category[]
//   GET /productos/buscar?categoria=&talle=&color=               -> Product[]
//        (solo activos y con variantes con stock > 0)
import { createFileRoute, Link } from "@tanstack/react-router";
import { useState } from "react";
import { useQuery } from "@tanstack/react-query";
import { api } from "@/lib/api";
import type { Category, Product } from "@/lib/types";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { Button } from "@/components/ui/button";

export const Route = createFileRoute("/_customer/productos")({
  component: SearchProductsPage,
});

function SearchProductsPage() {
  const [categoria, setCategoria] = useState<string>("");
  const [talle, setTalle] = useState("");
  const [color, setColor] = useState("");

  const cats = useQuery({ queryKey: ["categorias"], queryFn: () => api<Category[]>("/categorias") });

  const params = new URLSearchParams();
  if (categoria) params.set("categoria", categoria);
  if (talle) params.set("talle", talle);
  if (color) params.set("color", color);

  const { data, isLoading } = useQuery({
    queryKey: ["productos-buscar", categoria, talle, color],
    queryFn: () => api<Product[]>(`/productos/buscar?${params.toString()}`),
  });

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-semibold">Productos</h1>

      <Card>
        <CardHeader>
          <CardTitle>Filtros</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 gap-3 sm:grid-cols-4">
            <div className="space-y-2">
              <Label>Categoría</Label>
              <Select value={categoria} onValueChange={setCategoria}>
                <SelectTrigger>
                  <SelectValue placeholder="Todas" />
                </SelectTrigger>
                <SelectContent>
                  {cats.data?.map((c) => (
                    <SelectItem key={c.id} value={String(c.id)}>
                      {c.nombre}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>
            <div className="space-y-2">
              <Label>Talle</Label>
              <Input value={talle} onChange={(e) => setTalle(e.target.value)} />
            </div>
            <div className="space-y-2">
              <Label>Color</Label>
              <Input value={color} onChange={(e) => setColor(e.target.value)} />
            </div>
            <div className="flex items-end">
              <Button
                variant="outline"
                className="w-full"
                onClick={() => {
                  setCategoria("");
                  setTalle("");
                  setColor("");
                }}
              >
                Limpiar
              </Button>
            </div>
          </div>
        </CardContent>
      </Card>

      {isLoading && <p className="text-sm text-muted-foreground">Cargando…</p>}
      {data && (
        <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">
          {data.map((p) => (
            <Link key={p.id} to="/productos/$id" params={{ id: String(p.id) }}>
              <Card className="h-full transition-colors hover:bg-accent">
                <CardHeader>
                  <CardTitle className="text-base">{p.nombre}</CardTitle>
                </CardHeader>
                <CardContent>
                  <p className="text-sm text-muted-foreground line-clamp-2">{p.descripcion}</p>
                  <p className="mt-3 text-lg font-semibold">${p.precio_base.toFixed(2)}</p>
                </CardContent>
              </Card>
            </Link>
          ))}
          {data.length === 0 && (
            <p className="col-span-full text-center text-muted-foreground">
              No hay productos para esos filtros.
            </p>
          )}
        </div>
      )}
    </div>
  );
}
