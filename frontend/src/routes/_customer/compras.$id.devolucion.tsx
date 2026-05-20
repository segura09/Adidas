// HU13 — Solicitar devolución
// Endpoints backend:
//   GET  /compras/{id}                            -> Purchase  (para listar items)
//   POST /compras/{id}/devoluciones               -> Return
//        body: { motivo, items: [{ variante_id, cantidad }] }
import { createFileRoute, useParams, useNavigate } from "@tanstack/react-router";
import { useState, type FormEvent } from "react";
import { useQuery, useMutation } from "@tanstack/react-query";
import { api } from "@/lib/api";
import type { Purchase } from "@/lib/types";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { Label } from "@/components/ui/label";
import { Checkbox } from "@/components/ui/checkbox";

export const Route = createFileRoute("/_customer/compras/$id/devolucion")({
  component: ReturnPage,
});

function ReturnPage() {
  const { id } = useParams({ from: "/_customer/compras/$id/devolucion" });
  const navigate = useNavigate();
  const { data } = useQuery({
    queryKey: ["compra", id],
    queryFn: () => api<Purchase>(`/compras/${id}`),
  });

  const [motivo, setMotivo] = useState("");
  const [selected, setSelected] = useState<Record<number, number>>({});

  const create = useMutation({
    mutationFn: () =>
      api(`/compras/${id}/devoluciones`, {
        method: "POST",
        body: {
          motivo,
          items: Object.entries(selected)
            .filter(([, q]) => q > 0)
            .map(([varId, q]) => ({ variante_id: Number(varId), cantidad: q })),
        },
      }),
    onSuccess: () => navigate({ to: "/compras/$id", params: { id } }),
  });

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-semibold">Solicitar devolución · Compra #{id}</h1>

      <Card>
        <CardHeader>
          <CardTitle>Items a devolver</CardTitle>
        </CardHeader>
        <CardContent className="space-y-3">
          {data?.items.map((it) => {
            const chosen = selected[it.variante_id] ?? 0;
            return (
              <div
                key={it.variante_id}
                className="flex flex-col gap-2 rounded-md border p-3 sm:flex-row sm:items-center sm:justify-between"
              >
                <div className="flex items-center gap-3">
                  <Checkbox
                    checked={chosen > 0}
                    onCheckedChange={(c) =>
                      setSelected((s) => ({ ...s, [it.variante_id]: c ? 1 : 0 }))
                    }
                  />
                  <div className="text-sm">
                    <p className="font-medium">{it.producto_nombre ?? `Var #${it.variante_id}`}</p>
                    <p className="text-muted-foreground">
                      {it.talle} · {it.color} · {it.cantidad} comprados
                    </p>
                  </div>
                </div>
                <div className="flex items-center gap-2">
                  <Label className="text-xs">Cantidad</Label>
                  <Input
                    type="number"
                    min={0}
                    max={it.cantidad}
                    value={chosen}
                    onChange={(e) =>
                      setSelected((s) => ({ ...s, [it.variante_id]: Number(e.target.value) }))
                    }
                    className="w-20"
                  />
                </div>
              </div>
            );
          })}
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>Motivo</CardTitle>
        </CardHeader>
        <CardContent>
          <form
            onSubmit={(e: FormEvent) => {
              e.preventDefault();
              create.mutate();
            }}
            className="space-y-3"
          >
            <Textarea value={motivo} onChange={(e) => setMotivo(e.target.value)} required />
            <Button type="submit" disabled={create.isPending}>
              {create.isPending ? "Enviando…" : "Solicitar devolución"}
            </Button>
            {create.error && (
              <p className="text-sm text-destructive">{(create.error as Error).message}</p>
            )}
          </form>
        </CardContent>
      </Card>
    </div>
  );
}
