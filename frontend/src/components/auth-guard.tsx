import { useEffect, type ReactNode } from "react";
import { useNavigate } from "@tanstack/react-router";
import { useAuth } from "@/hooks/use-auth";

interface Props {
  children: ReactNode;
  requireAdmin?: boolean;
}

export function AuthGuard({ children, requireAdmin = false }: Props) {
  const navigate = useNavigate();
  const { hydrated, isAuthenticated, user } = useAuth();

  useEffect(() => {
    if (!hydrated) return;
    if (!isAuthenticated) {
      navigate({ to: "/login" });
      return;
    }
    if (requireAdmin && !user?.isAdmin) {
      navigate({ to: "/productos" });
    }
    if (!requireAdmin && user?.isAdmin) {
      // admins navegan por el panel
      navigate({ to: "/admin" });
    }
  }, [hydrated, isAuthenticated, user, requireAdmin, navigate]);

  if (!hydrated || !isAuthenticated) {
    return (
      <div className="flex min-h-screen items-center justify-center text-muted-foreground">
        Cargando…
      </div>
    );
  }
  if (requireAdmin && !user?.isAdmin) return null;
  return <>{children}</>;
}
