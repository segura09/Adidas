import type { Product } from "./types";
import { API_URL } from "./api";

const productImages: Record<string, string> = {
  "F50 LEAGUE": "/products/f50-league.png",
  "RESPONSE RUNNER": "/products/response-runner.png",
  "remera de ARGENTINA": "/products/remera-argentina.png",
  "remera ALTERNATIVA DE ARGENTINA": "/products/remera-alternativa-argentina.png",
};

export function getProductImage(product: Pick<Product, "nombre" | "image_url">): string | null {
  if (product.image_url) {
    if (product.image_url.startsWith("http")) return product.image_url;
    const apiOrigin = API_URL.replace(/\/api\/?$/, "");
    return `${apiOrigin}${product.image_url}`;
  }

  return productImages[product.nombre] ?? null;
}
