// HU12 — Detalle de producto + reseñas
// Endpoints backend:
//   GET  /productos/{id}                       -> Product
//   GET  /productos/{id}/variantes             -> Variant[]
//   GET  /productos/{id}/resenas               -> Review[]
//   GET  /productos/{id}/resenas/resumen       -> ReviewSummary { promedio, cantidad }
//   POST /productos/{id}/resenas               -> Review  body: { puntaje, comentario }
//   POST /carritos/items                       -> Cart    body: { variante_id, cantidad }
import { createFileRoute, useNavigate, useParams } from "@tanstack/react-router";
import { useState } from "react";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { api } from "@/lib/api";
import { getToken } from "@/lib/auth";
import { useAuth } from "@/hooks/use-auth";
import { getProductImage } from "@/lib/product-images";
import type { Product, Variant, Review, ReviewSummary } from "@/lib/types";
import { Button } from "@/components/ui/button";
import { Label } from "@/components/ui/label";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { Star } from "lucide-react";

export const Route = createFileRoute("/_customer/productos/$id")({
  component: ProductDetailPage,
});

function ProductDetailPage() {
  const { id } = useParams({ from: "/_customer/productos/$id" });
  const navigate = useNavigate();
  const qc = useQueryClient();
  const { user } = useAuth();
  const [varianteId, setVarianteId] = useState<string>("");
  const [cantidad, setCantidad] = useState(1);

  const prod = useQuery({ queryKey: ["producto", id], queryFn: () => api<Product>(`/productos/${id}`) });
  const variants = useQuery({
    queryKey: ["variantes", id],
    queryFn: () => api<Variant[]>(`/productos/${id}/variantes`),
  });
  const reviews = useQuery({
    queryKey: ["resenas", id],
    queryFn: () => api<Review[]>(`/productos/${id}/resenas`),
  });
  const summary = useQuery({
    queryKey: ["resenas-resumen", id],
    queryFn: () => api<ReviewSummary>(`/productos/${id}/resenas/resumen`),
  });

  const addToCart = useMutation({
    mutationFn: () => {
      if (!getToken()) {
        navigate({ to: "/login" });
        throw new Error("Inicia sesion para agregar productos al carrito.");
      }
      return api("/carritos/items", {
        method: "POST",
        body: { variante_id: Number(varianteId), cantidad },
      });
    },
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ["carrito"] });
      navigate({ to: "/carrito" });
    },
  });

  const currentClienteId = user?.cliente_id ?? user?.id;
  const visibleReviews = reviews.data?.filter((r) => r.cliente_id !== currentClienteId) ?? [];

  return (
    <div className="space-y-6">
      {prod.data && (
        <Card>
          <CardHeader>
            <CardTitle className="text-2xl">{prod.data.nombre}</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            {getProductImage(prod.data) && (
              <div className="aspect-[4/3] overflow-hidden rounded-md bg-muted sm:aspect-[16/9]">
                <img
                  src={getProductImage(prod.data)!}
                  alt={prod.data.nombre}
                  className="h-full w-full object-contain p-6"
                />
              </div>
            )}
            <p className="text-sm text-muted-foreground">{prod.data.descripcion}</p>
            <p className="text-2xl font-semibold">${prod.data.precio_base.toFixed(2)}</p>
            {summary.data && (
              <div className="flex items-center gap-2 text-sm">
                <Star className="size-4 fill-yellow-500 text-yellow-500" />
                <span>{summary.data.promedio.toFixed(1)}</span>
                <span className="text-muted-foreground">({summary.data.cantidad} reseñas)</span>
              </div>
            )}

            <div className="grid grid-cols-1 gap-3 sm:grid-cols-3">
              <div className="space-y-2 sm:col-span-2">
                <Label>Variante</Label>
                <Select value={varianteId} onValueChange={setVarianteId}>
                  <SelectTrigger>
                    <SelectValue placeholder="Elegir talle / color" />
                  </SelectTrigger>
                  <SelectContent>
                    {variants.data?.map((v) => (
                      <SelectItem key={v.id} value={String(v.id)} disabled={v.stock <= 0}>
                        {v.talle} · {v.color} {v.stock <= 0 ? "(sin stock)" : `· ${v.stock} u.`}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>
              <div className="space-y-2">
                <Label>Cantidad</Label>
                <input
                  type="number"
                  min={1}
                  value={cantidad}
                  onChange={(e) => setCantidad(Number(e.target.value))}
                  className="flex h-9 w-full rounded-md border border-input bg-transparent px-3 py-1 text-sm"
                />
              </div>
            </div>
            <Button onClick={() => addToCart.mutate()} disabled={!varianteId || addToCart.isPending}>
              {addToCart.isPending ? "Agregando…" : "Agregar al carrito"}
            </Button>
            {addToCart.error && (
              <p className="text-sm text-destructive">{(addToCart.error as Error).message}</p>
            )}
          </CardContent>
        </Card>
      )}

      <Card>
        <CardHeader>
          <CardTitle>Reseñas</CardTitle>
        </CardHeader>
        <CardContent className="space-y-3">
          {visibleReviews.length === 0 && (
            <p className="text-sm text-muted-foreground">Aún no hay reseñas.</p>
          )}
          {visibleReviews.map((r) => (
            <div key={r.id} className="rounded-md border p-3">
              <div className="flex items-center gap-2 text-sm">
                <Star className="size-4 fill-yellow-500 text-yellow-500" />
                <strong>{r.puntaje}</strong>
                <span>{r.cliente_nombre ?? "Cliente"}</span>
                <span className="text-muted-foreground">· {new Date(r.fecha).toLocaleDateString()}</span>
              </div>
              {r.comentario && <p className="mt-2 text-sm">{r.comentario}</p>}
            </div>
          ))}
        </CardContent>
      </Card>
    </div>
  );
}
