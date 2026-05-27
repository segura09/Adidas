// HU5 + HU6 — Checkout (con cupón opcional)
// Endpoints backend:
//   GET  /carritos/me                                  -> Cart
//   POST /cupones/validar  body: { codigo }            -> { porcentaje_descuento, valido: boolean }
//   POST /compras          body: { cupon_codigo? }     -> Purchase
//        (crea compra a partir del carrito, valida stock, reserva,
//         calcula total con descuento y consume el cupón si aplica)
import { createFileRoute, useNavigate } from "@tanstack/react-router";
import { useState } from "react";
import { useQuery, useMutation } from "@tanstack/react-query";
import { api } from "@/lib/api";
import type { Cart, Purchase } from "@/lib/types";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { AuthGuard } from "@/components/auth-guard";

export const Route = createFileRoute("/_customer/checkout")({
  component: ProtectedCheckoutPage,
});

function ProtectedCheckoutPage() {
  return (
    <AuthGuard>
      <CheckoutPage />
    </AuthGuard>
  );
}

function CheckoutPage() {
  const navigate = useNavigate();
  const [codigo, setCodigo] = useState("");
  const [cuponAplicado, setCuponAplicado] = useState("");
  const [descuentoPct, setDescuentoPct] = useState<number>(0);
  const [cuponMsg, setCuponMsg] = useState<string | null>(null);

  const { data: cart } = useQuery({
    queryKey: ["carrito"],
    queryFn: () => api<Cart>("/carritos/me"),
  });

  const subtotal =
    cart?.items.reduce((acc, it) => acc + (it.precio_unitario ?? 0) * it.cantidad, 0) ?? 0;
  const descuento = subtotal * (descuentoPct / 100);
  const total = subtotal - descuento;

  const validar = useMutation({
    mutationFn: () =>
      api<{ porcentaje_descuento: number; valido: boolean }>("/cupones/validar", {
        method: "POST",
        body: { codigo: normalizarCodigo(codigo) },
      }),
    onSuccess: (res) => {
      if (res.valido) {
        setDescuentoPct(res.porcentaje_descuento);
        setCuponAplicado(normalizarCodigo(codigo));
        setCuponMsg(`Cupón aplicado: ${res.porcentaje_descuento}% off`);
      } else {
        setDescuentoPct(0);
        setCuponAplicado("");
        setCuponMsg("Cupón inválido o vencido");
      }
    },
    onError: (e) => {
      setDescuentoPct(0);
      setCuponAplicado("");
      setCuponMsg((e as Error).message);
    },
  });

  const confirmar = useMutation({
    mutationFn: () =>
      api<Purchase>("/compras", {
        method: "POST",
        body: cuponAplicado ? { codigo_cupon: cuponAplicado } : {},
      }),
    onSuccess: (p) => navigate({ to: "/compras/$id", params: { id: String(p.id) } }),
  });

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-semibold">Checkout</h1>

      <Card>
        <CardHeader>
          <CardTitle>Cupón de descuento</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="flex flex-col gap-3 sm:flex-row sm:items-end">
            <div className="flex-1 space-y-2">
              <Label>Código</Label>
              <Input
                value={codigo}
                onChange={(e) => {
                  setCodigo(e.target.value);
                  setCuponAplicado("");
                  setDescuentoPct(0);
                  setCuponMsg(null);
                }}
              />
            </div>
            <Button
              variant="outline"
              onClick={() => validar.mutate()}
              disabled={!normalizarCodigo(codigo) || validar.isPending}
            >
              Aplicar
            </Button>
          </div>
          {cuponMsg && <p className="mt-2 text-sm text-muted-foreground">{cuponMsg}</p>}
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>Resumen</CardTitle>
        </CardHeader>
        <CardContent className="space-y-2">
          <Row label="Subtotal" value={`$${subtotal.toFixed(2)}`} />
          <Row label={`Descuento (${descuentoPct}%)`} value={`- $${descuento.toFixed(2)}`} />
          <div className="my-2 border-t" />
          <Row label="Total" value={`$${total.toFixed(2)}`} bold />
          <Button
            className="mt-4 w-full"
            onClick={() => confirmar.mutate()}
            disabled={!cart || cart.items.length === 0 || confirmar.isPending}
          >
            {confirmar.isPending ? "Procesando…" : "Confirmar compra"}
          </Button>
          {confirmar.error && (
            <p className="text-sm text-destructive">{(confirmar.error as Error).message}</p>
          )}
        </CardContent>
      </Card>
    </div>
  );
}

function Row({ label, value, bold }: { label: string; value: string; bold?: boolean }) {
  return (
    <div className={"flex justify-between " + (bold ? "text-lg font-semibold" : "text-sm")}>
      <span className={bold ? "" : "text-muted-foreground"}>{label}</span>
      <span>{value}</span>
    </div>
  );
}

function normalizarCodigo(codigo: string) {
  return codigo.trim().toUpperCase();
}
