// HU12 — Detalle de producto + reseñas
// Endpoints backend:
//   GET  /productos/{id}                       -> Product
//   GET  /productos/{id}/variantes             -> Variant[]
//   GET  /productos/{id}/resenas               -> Review[]
//   GET  /productos/{id}/resenas/resumen       -> ReviewSummary { promedio, cantidad }
//   POST /productos/{id}/resenas               -> Review  body: { puntaje, comentario }
//   POST /carritos/items                       -> Cart    body: { variante_id, cantidad }
import { createFileRoute, useNavigate, useParams } from "@tanstack/react-router";
import { useState, type FormEvent } from "react";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { api } from "@/lib/api";
import type { Product, Variant, Review, ReviewSummary } from "@/lib/types";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
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
  const [varianteId, setVarianteId] = useState<string>("");
  const [cantidad, setCantidad] = useState(1);
  const [puntaje, setPuntaje] = useState(5);
  const [comentario, setComentario] = useState("");

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
    mutationFn: () =>
      api("/carritos/items", {
        method: "POST",
        body: { variante_id: Number(varianteId), cantidad },
      }),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ["carrito"] });
      navigate({ to: "/carrito" });
    },
  });

  const createReview = useMutation({
    mutationFn: () =>
      api(`/productos/${id}/resenas`, {
        method: "POST",
        body: { puntaje, comentario },
      }),
    onSuccess: () => {
      setComentario("");
      qc.invalidateQueries({ queryKey: ["resenas", id] });
      qc.invalidateQueries({ queryKey: ["resenas-resumen", id] });
    },
  });

  return (
    <div className="space-y-6">
      {prod.data && (
        <Card>
          <CardHeader>
            <CardTitle className="text-2xl">{prod.data.nombre}</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
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
          <CardTitle>Dejar una reseña</CardTitle>
        </CardHeader>
        <CardContent>
          <form
            onSubmit={(e: FormEvent) => {
              e.preventDefault();
              createReview.mutate();
            }}
            className="space-y-3"
          >
            <div className="space-y-2">
              <Label>Puntaje</Label>
              <Select value={String(puntaje)} onValueChange={(v) => setPuntaje(Number(v))}>
                <SelectTrigger className="w-32">
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  {[1, 2, 3, 4, 5].map((n) => (
                    <SelectItem key={n} value={String(n)}>
                      {n} ★
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>
            <div className="space-y-2">
              <Label>Comentario</Label>
              <Textarea value={comentario} onChange={(e) => setComentario(e.target.value)} />
            </div>
            <Button type="submit" disabled={createReview.isPending}>
              {createReview.isPending ? "Enviando…" : "Enviar reseña"}
            </Button>
            {createReview.error && (
              <p className="text-sm text-destructive">{(createReview.error as Error).message}</p>
            )}
          </form>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>Reseñas</CardTitle>
        </CardHeader>
        <CardContent className="space-y-3">
          {reviews.data?.length === 0 && (
            <p className="text-sm text-muted-foreground">Aún no hay reseñas.</p>
          )}
          {reviews.data?.map((r) => (
            <div key={r.id} className="rounded-md border p-3">
              <div className="flex items-center gap-2 text-sm">
                <Star className="size-4 fill-yellow-500 text-yellow-500" />
                <strong>{r.puntaje}</strong>
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
