import { createFileRoute } from "@tanstack/react-router";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { useState } from "react";
import { api } from "@/lib/api";
import type { Purchase, PurchaseStatus } from "@/lib/types";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Label } from "@/components/ui/label";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";

export const Route = createFileRoute("/admin/compras")({
  component: AdminPurchasesPage,
});

const estados: (PurchaseStatus | "todos")[] = [
  "todos",
  "pendiente_pago",
  "pagada",
  "enviada",
  "entregada",
  "cancelada",
];

const estadoLabels: Record<PurchaseStatus | "todos", string> = {
  todos: "todos",
  pendiente_pago: "pendiente",
  pagada: "pagada",
  enviada: "enviada",
  entregada: "entregada",
  cancelada: "cancelada",
};

function AdminPurchasesPage() {
  const qc = useQueryClient();
  const [estado, setEstado] = useState<PurchaseStatus | "todos">("todos");
  const qs = estado !== "todos" ? `?estado=${estado}` : "";

  const compras = useQuery({
    queryKey: ["admin-compras", estado],
    queryFn: () => api<Purchase[]>(`/compras${qs}`),
  });

  const changeStatus = useMutation({
    mutationFn: ({ id, action }: { id: number; action: "pagar" | "enviar" | "entregar" | "cancelar" }) =>
      api<Purchase>(`/compras/${id}/${action}`, { method: "POST" }),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ["admin-compras"] });
    },
  });

  function actionsFor(compra: Purchase) {
    if (compra.estado === "pendiente_pago") {
      return ["pagar", "cancelar"] as const;
    }
    if (compra.estado === "pagada") {
      return ["enviar", "cancelar"] as const;
    }
    if (compra.estado === "enviada") {
      return ["entregar"] as const;
    }
    return [] as const;
  }

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-semibold">Compras</h1>

      <Card>
        <CardContent className="pt-6">
          <div className="flex max-w-xs flex-col gap-2">
            <Label>Filtrar por estado</Label>
            <Select value={estado} onValueChange={(value) => setEstado(value as PurchaseStatus | "todos")}>
              <SelectTrigger>
                <SelectValue />
              </SelectTrigger>
              <SelectContent>
                {estados.map((s) => (
                  <SelectItem key={s} value={s}>
                    {estadoLabels[s]}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>Listado</CardTitle>
        </CardHeader>
        <CardContent className="overflow-x-auto">
          {compras.isLoading && <p className="text-sm text-muted-foreground">Cargando...</p>}
          {compras.error && (
            <p className="text-sm text-destructive">{(compras.error as Error).message}</p>
          )}
          {compras.data && (
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>ID</TableHead>
                  <TableHead>Cliente</TableHead>
                  <TableHead>Fecha</TableHead>
                  <TableHead>Total</TableHead>
                  <TableHead>Estado</TableHead>
                  <TableHead className="text-right">Acciones</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {compras.data.map((compra) => (
                  <TableRow key={compra.id}>
                    <TableCell>{compra.id}</TableCell>
                    <TableCell>{compra.cliente_id}</TableCell>
                    <TableCell>{new Date(compra.fecha).toLocaleString()}</TableCell>
                    <TableCell>${compra.total.toFixed(2)}</TableCell>
                    <TableCell>
                      <Badge variant="secondary">{estadoLabels[compra.estado]}</Badge>
                    </TableCell>
                    <TableCell className="space-x-2 text-right">
                      {actionsFor(compra).map((action) => (
                        <Button
                          key={action}
                          size="sm"
                          variant={action === "cancelar" ? "destructive" : "default"}
                          disabled={changeStatus.isPending}
                          onClick={() => changeStatus.mutate({ id: compra.id, action })}
                        >
                          {action === "pagar" && "Confirmar pago"}
                          {action === "enviar" && "Marcar enviada"}
                          {action === "entregar" && "Marcar entregada"}
                          {action === "cancelar" && "Cancelar"}
                        </Button>
                      ))}
                    </TableCell>
                  </TableRow>
                ))}
                {compras.data.length === 0 && (
                  <TableRow>
                    <TableCell colSpan={6} className="text-center text-muted-foreground">
                      Sin compras.
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
