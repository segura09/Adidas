import { Link, Outlet, useRouterState } from "@tanstack/react-router";
import { CircleUser, LogIn, LogOut, Menu } from "lucide-react";
import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Sheet, SheetContent, SheetTrigger } from "@/components/ui/sheet";
import { clearAuth } from "@/lib/auth";
import { useNavigate } from "@tanstack/react-router";
import { useAuth } from "@/hooks/use-auth";

interface NavItem {
  to: string;
  label: string;
}

interface Props {
  title: string;
  items: NavItem[];
  children?: React.ReactNode;
}

export function AppShell({ title, items }: Props) {
  const navigate = useNavigate();
  const [open, setOpen] = useState(false);
  const path = useRouterState({ select: (s) => s.location.pathname });
  const { hydrated, isAuthenticated, user } = useAuth();
  const accountLabel = hydrated && isAuthenticated ? user?.email : "Invitado";

  function logout() {
    clearAuth();
    navigate({ to: "/productos" });
  }

  function login() {
    navigate({ to: "/login" });
  }

  const nav = (
    <nav className="flex flex-col gap-1">
      {items.map((it) => {
        const active = path === it.to || path.startsWith(it.to + "/");
        return (
          <Link
            key={it.to}
            to={it.to}
            onClick={() => setOpen(false)}
            className={
              "rounded-md px-3 py-2 text-sm transition-colors " +
              (active
                ? "bg-primary text-primary-foreground"
                : "text-foreground hover:bg-muted")
            }
          >
            {it.label}
          </Link>
        );
      })}
    </nav>
  );

  return (
    <div className="flex min-h-screen flex-col bg-muted/30 md:flex-row">
      {/* Sidebar desktop */}
      <aside className="hidden w-64 shrink-0 border-r bg-background p-4 md:flex md:flex-col">
        <Link to="/" className="mb-6 text-lg font-semibold">
          {title}
        </Link>
        {nav}
        <div className="mt-auto pt-4">
          <div className="mb-3 flex min-w-0 items-center gap-2 rounded-md border px-3 py-2 text-sm">
            <CircleUser className="size-4 shrink-0 text-muted-foreground" />
            <span className="min-w-0 truncate">{accountLabel}</span>
          </div>
          {hydrated && isAuthenticated ? (
            <Button variant="outline" className="w-full" onClick={logout}>
              <LogOut className="size-4" /> Salir
            </Button>
          ) : (
            <Button variant="outline" className="w-full" onClick={login}>
              <LogIn className="size-4" /> Iniciar sesion
            </Button>
          )}
        </div>
      </aside>

      {/* Header mobile */}
      <header className="flex items-center justify-between border-b bg-background px-4 py-3 md:hidden">
        <Link to="/" className="font-semibold">
          {title}
        </Link>
        <div className="mx-3 min-w-0 flex-1 truncate text-right text-xs text-muted-foreground">
          {accountLabel}
        </div>
        <Sheet open={open} onOpenChange={setOpen}>
          <SheetTrigger asChild>
            <Button variant="ghost" size="icon">
              <Menu className="size-5" />
            </Button>
          </SheetTrigger>
          <SheetContent side="left" className="w-64 p-4">
            <p className="mb-6 text-lg font-semibold">{title}</p>
            <div className="mb-4 flex min-w-0 items-center gap-2 rounded-md border px-3 py-2 text-sm">
              <CircleUser className="size-4 shrink-0 text-muted-foreground" />
              <span className="min-w-0 truncate">{accountLabel}</span>
            </div>
            {nav}
            <div className="mt-6">
              {hydrated && isAuthenticated ? (
                <Button variant="outline" className="w-full" onClick={logout}>
                  <LogOut className="size-4" /> Salir
                </Button>
              ) : (
                <Button variant="outline" className="w-full" onClick={login}>
                  <LogIn className="size-4" /> Iniciar sesion
                </Button>
              )}
            </div>
          </SheetContent>
        </Sheet>
      </header>

      <main className="flex-1 p-4 md:p-8">
        <div className="mb-6 hidden items-center justify-end md:flex">
          <div className="flex max-w-xs items-center gap-2 rounded-md border bg-background px-3 py-2 text-sm">
            <CircleUser className="size-4 shrink-0 text-muted-foreground" />
            <span className="min-w-0 truncate">{accountLabel}</span>
          </div>
        </div>
        <Outlet />
      </main>
    </div>
  );
}
