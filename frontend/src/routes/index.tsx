import { createFileRoute, useNavigate } from "@tanstack/react-router";
import { useEffect } from "react";
import { useAuth } from "@/hooks/use-auth";

export const Route = createFileRoute("/")({
  component: Index,
});

function Index() {
  const navigate = useNavigate();
  const { hydrated, isAuthenticated, user } = useAuth();

  useEffect(() => {
    if (!hydrated) return;
    if (!isAuthenticated) {
      navigate({ to: "/login" });
    } else if (user?.isAdmin) {
      navigate({ to: "/admin" });
    } else {
      navigate({ to: "/productos" });
    }
  }, [hydrated, isAuthenticated, user, navigate]);

  return (
    <div className="flex min-h-screen items-center justify-center bg-background text-muted-foreground">
      Cargando…
    </div>
  );
}
