// HU1 — Productos (ABM)
// Endpoints backend:
//   GET    /productos              -> Product[]
//   GET    /categorias             -> Category[]
//   POST   /productos              -> Product  body: { nombre, descripcion, precio_base, categoria_id }
//   PUT    /productos/{id}         -> Product  body: parcial
//   DELETE /productos/{id}         -> baja lógica (activo=false)
import { createFileRoute, Link, Outlet, useRouterState } from "@tanstack/react-router";
import { useState, type FormEvent } from "react";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { api, API_URL } from "@/lib/api";
import { getToken } from "@/lib/auth";
import { getProductImage } from "@/lib/product-images";
import type { Category, Product, Variant } from "@/lib/types";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { Badge } from "@/components/ui/badge";

export const Route = createFileRoute("/admin/productos")({
  component: ProductsPage,
});

interface FormState {
  nombre: string;
  descripcion: string;
  precio_base: string;
  categoria_id: string;
  talle: string;
  color: string;
  stock: string;
  sku: string;
}

const empty: FormState = {
  nombre: "",
  descripcion: "",
  precio_base: "",
  categoria_id: "",
  talle: "",
  color: "",
  stock: "1",
  sku: "",
};

function ProductsPage() {
  const isChildRoute = useRouterState({
    select: (state) => state.location.pathname !== "/admin/productos",
  });
  const qc = useQueryClient();
  const [form, setForm] = useState<FormState>(empty);
  const [imageFile, setImageFile] = useState<File | null>(null);

  const cats = useQuery({ queryKey: ["categorias"], queryFn: () => api<Category[]>("/categorias") });
  const prods = useQuery({ queryKey: ["productos"], queryFn: () => api<Product[]>("/productos") });

  const create = useMutation({
    mutationFn: async (data: FormState) => {
      const product = await api<Product>("/productos", {
        method: "POST",
        body: {
          nombre: data.nombre,
          descripcion: data.descripcion || null,
          precio_base: Number(data.precio_base),
          categoria_id: Number(data.categoria_id),
        },
      });

      await api<Variant>(`/productos/${product.id}/variantes`, {
        method: "POST",
        body: {
          talle: data.talle,
          color: data.color,
          stock: Number(data.stock),
          sku: data.sku || buildSku(product.nombre, data.talle, data.color),
        },
      });

      if (imageFile) {
        await uploadProductImage(product.id, imageFile);
      }

      return product;
    },
    onSuccess: () => {
      setForm(empty);
      setImageFile(null);
      qc.invalidateQueries({ queryKey: ["productos"] });
    },
  });

  const deactivate = useMutation({
    mutationFn: (id: number) => api(`/productos/${id}`, { method: "DELETE" }),
    onSuccess: () => qc.invalidateQueries({ queryKey: ["productos"] }),
  });

  const uploadImage = useMutation({
    mutationFn: ({ productId, file }: { productId: number; file: File }) =>
      uploadProductImage(productId, file),
    onSuccess: () => qc.invalidateQueries({ queryKey: ["productos"] }),
  });

  function onSubmit(e: FormEvent) {
    e.preventDefault();
    create.mutate(form);
  }

  if (isChildRoute) {
    return <Outlet />;
  }

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-semibold">Productos</h1>

      <Card>
        <CardHeader>
          <CardTitle>Nuevo producto</CardTitle>
        </CardHeader>
        <CardContent>
          <form onSubmit={onSubmit} className="grid grid-cols-1 gap-3 md:grid-cols-2">
            <div className="space-y-2">
              <Label>Nombre</Label>
              <Input
                value={form.nombre}
                onChange={(e) => setForm({ ...form, nombre: e.target.value })}
                required
              />
            </div>
            <div className="space-y-2">
              <Label>Precio base</Label>
              <Input
                type="number"
                min="0.01"
                step="0.01"
                value={form.precio_base}
                onChange={(e) => setForm({ ...form, precio_base: e.target.value })}
                required
              />
            </div>
            <div className="space-y-2 md:col-span-2">
              <Label>Descripción</Label>
              <Textarea
                value={form.descripcion}
                onChange={(e) => setForm({ ...form, descripcion: e.target.value })}
              />
            </div>
            <div className="space-y-2">
              <Label>Categoría</Label>
              <Select
                value={form.categoria_id}
                onValueChange={(v) => setForm({ ...form, categoria_id: v })}
              >
                <SelectTrigger>
                  <SelectValue placeholder="Elegir…" />
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
              <Input
                value={form.talle}
                onChange={(e) => setForm({ ...form, talle: e.target.value })}
                placeholder="Ej: 40, M, L"
                required
              />
            </div>
            <div className="space-y-2">
              <Label>Color</Label>
              <Input
                value={form.color}
                onChange={(e) => setForm({ ...form, color: e.target.value })}
                placeholder="Ej: Negro"
                required
              />
            </div>
            <div className="space-y-2">
              <Label>Stock inicial</Label>
              <Input
                type="number"
                min="0"
                value={form.stock}
                onChange={(e) => setForm({ ...form, stock: e.target.value })}
                required
              />
            </div>
            <div className="space-y-2">
              <Label>SKU</Label>
              <Input
                value={form.sku}
                onChange={(e) => setForm({ ...form, sku: e.target.value })}
                placeholder="Opcional"
              />
            </div>
            <div className="space-y-2 md:col-span-2">
              <Label>Imagen</Label>
              <Input
                type="file"
                accept="image/png,image/jpeg,image/webp"
                onChange={(e) => setImageFile(e.target.files?.[0] ?? null)}
              />
            </div>
            <div className="flex items-end md:col-span-2">
              <Button type="submit" disabled={create.isPending}>
                {create.isPending ? "Creando…" : "Crear producto"}
              </Button>
            </div>
            {create.error && (
              <p className="text-sm text-destructive md:col-span-2">
                {(create.error as Error).message}
              </p>
            )}
          </form>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>Listado</CardTitle>
        </CardHeader>
        <CardContent className="overflow-x-auto">
          {prods.isLoading && <p className="text-sm text-muted-foreground">Cargando…</p>}
          {prods.data && (
            <Table>
              <TableHeader>
                  <TableRow>
                  <TableHead>Imagen</TableHead>
                  <TableHead>ID</TableHead>
                  <TableHead>Nombre</TableHead>
                  <TableHead>Precio</TableHead>
                  <TableHead>Estado</TableHead>
                  <TableHead className="text-right">Acciones</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {prods.data.map((p) => (
                  <TableRow key={p.id}>
                    <TableCell>
                      {getProductImage(p) ? (
                        <img
                          src={getProductImage(p)!}
                          alt={p.nombre}
                          className="h-12 w-12 rounded-md object-contain"
                        />
                      ) : (
                        <span className="text-xs text-muted-foreground">Sin imagen</span>
                      )}
                    </TableCell>
                    <TableCell>{p.id}</TableCell>
                    <TableCell>{p.nombre}</TableCell>
                    <TableCell>${p.precio_base.toFixed(2)}</TableCell>
                    <TableCell>
                      {p.activo ? (
                        <Badge>Activo</Badge>
                      ) : (
                        <Badge variant="secondary">Inactivo</Badge>
                      )}
                    </TableCell>
                    <TableCell className="space-x-2 text-right">
                      <Input
                        type="file"
                        accept="image/png,image/jpeg,image/webp"
                        className="inline-flex max-w-44"
                        disabled={uploadImage.isPending}
                        onChange={(e) => {
                          const file = e.target.files?.[0];
                          if (file) uploadImage.mutate({ productId: p.id, file });
                          e.target.value = "";
                        }}
                      />
                      <Button asChild size="sm" variant="outline">
                        <Link to="/admin/productos/$id/variantes" params={{ id: String(p.id) }}>
                          Variantes
                        </Link>
                      </Button>
                      {p.activo && (
                        <Button
                          size="sm"
                          variant="destructive"
                          onClick={() => deactivate.mutate(p.id)}
                        >
                          Dar de baja
                        </Button>
                      )}
                    </TableCell>
                  </TableRow>
                ))}
                {prods.data.length === 0 && (
                  <TableRow>
                    <TableCell colSpan={6} className="text-center text-muted-foreground">
                      Sin productos cargados.
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

function buildSku(nombre: string, talle: string, color: string) {
  const base = `${nombre}-${talle}-${color}`
    .toUpperCase()
    .replace(/[^A-Z0-9]+/g, "-")
    .replace(/^-|-$/g, "")
    .slice(0, 40);

  return `${base}-${Date.now().toString().slice(-6)}`;
}

async function uploadProductImage(productId: number, file: File) {
  const formData = new FormData();
  formData.append("file", file);

  const token = getToken();
  const headers: Record<string, string> = {};
  if (token) headers.Authorization = `Bearer ${token}`;

  const res = await fetch(`${API_URL}/productos/${productId}/imagen`, {
    method: "POST",
    headers,
    body: formData,
  });

  if (!res.ok) {
    const text = await res.text();
    throw new Error(text || "No se pudo subir la imagen");
  }
}
