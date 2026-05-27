// HU3 — Buscar productos (cliente)
// Endpoints backend:
//   GET /categorias                                              -> Category[]
//   GET /productos/buscar?categoria=&talle=&color=               -> Product[]
//        (solo activos y con variantes con stock > 0)
import { createFileRoute, Outlet, useRouterState } from "@tanstack/react-router";
import { useState } from "react";
import { useQuery } from "@tanstack/react-query";
import { api } from "@/lib/api";
import { getProductImage } from "@/lib/product-images";
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
  const pathname = useRouterState({ select: (state) => state.location.pathname });

  if (pathname !== "/productos") {
    return <Outlet />;
  }

  return <ProductListPage />;
}

function ProductListPage() {
  const [categoria, setCategoria] = useState<string>("");
  const [producto, setProducto] = useState("");
  const [precioMinDraft, setPrecioMinDraft] = useState("");
  const [precioMaxDraft, setPrecioMaxDraft] = useState("");
  const [precioMin, setPrecioMin] = useState("");
  const [precioMax, setPrecioMax] = useState("");

  const cats = useQuery({ queryKey: ["categorias"], queryFn: () => api<Category[]>("/categorias") });

  const params = new URLSearchParams();
  if (categoria) params.set("categoria", categoria);

  const { data, isLoading } = useQuery({
    queryKey: ["productos-buscar", categoria],
    queryFn: () => api<Product[]>(`/productos/buscar?${params.toString()}`),
  });

  const productSearch = producto.trim().toLowerCase();
  const min = precioMin ? Number(precioMin) : null;
  const max = precioMax ? Number(precioMax) : null;
  const filteredProducts =
    data?.filter((p) => {
      const matchesName = p.nombre.toLowerCase().includes(productSearch);
      const matchesMin = min === null || p.precio_base >= min;
      const matchesMax = max === null || p.precio_base <= max;
      return matchesName && matchesMin && matchesMax;
    }) ?? [];

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-semibold">Productos</h1>

      <Card>
        <CardHeader>
          <CardTitle>Filtros</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 gap-3 md:grid-cols-3 xl:grid-cols-6">
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
              <Label>Producto</Label>
              <Input
                value={producto}
                onChange={(e) => setProducto(e.target.value)}
                placeholder="Buscar por nombre"
              />
            </div>
            <div className="space-y-2">
              <Label>Precio minimo</Label>
              <Input
                type="number"
                min={0}
                value={precioMinDraft}
                onChange={(e) => setPrecioMinDraft(e.target.value)}
                placeholder="0"
              />
            </div>
            <div className="space-y-2">
              <Label>Precio maximo</Label>
              <Input
                type="number"
                min={0}
                value={precioMaxDraft}
                onChange={(e) => setPrecioMaxDraft(e.target.value)}
                placeholder="Sin limite"
              />
            </div>
            <div className="flex items-end">
              <Button
                variant="secondary"
                className="w-full"
                onClick={() => {
                  setPrecioMin(precioMinDraft);
                  setPrecioMax(precioMaxDraft);
                }}
              >
                Filtrar precio
              </Button>
            </div>
            <div className="flex items-end">
              <Button
                variant="outline"
                className="w-full"
                onClick={() => {
                  setCategoria("");
                  setProducto("");
                  setPrecioMinDraft("");
                  setPrecioMaxDraft("");
                  setPrecioMin("");
                  setPrecioMax("");
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
          {filteredProducts.map((p) => (
            <Card key={p.id} className="h-full transition-colors hover:bg-accent">
              {getProductImage(p) && (
                <div className="aspect-square overflow-hidden rounded-t-lg bg-muted">
                  <img
                    src={getProductImage(p)!}
                    alt={p.nombre}
                    className="h-full w-full object-contain p-4"
                    loading="lazy"
                  />
                </div>
              )}
              <CardHeader>
                <CardTitle className="text-base">{p.nombre}</CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-sm text-muted-foreground line-clamp-2">{p.descripcion}</p>
                <p className="mt-3 text-lg font-semibold">${p.precio_base.toFixed(2)}</p>
                <Button asChild className="mt-4 w-full" size="sm">
                  <a href={`/productos/${p.id}`}>Ver producto</a>
                </Button>
              </CardContent>
            </Card>
          ))}
          {filteredProducts.length === 0 && (
            <p className="col-span-full text-center text-muted-foreground">
              No hay productos para esos filtros.
            </p>
          )}
        </div>
      )}
    </div>
  );
}
