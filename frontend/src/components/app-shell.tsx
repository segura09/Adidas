import { Link, Outlet, useRouterState } from "@tanstack/react-router";
import { Menu, LogOut } from "lucide-react";
import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Sheet, SheetContent, SheetTrigger } from "@/components/ui/sheet";
import { clearAuth } from "@/lib/auth";
import { useNavigate } from "@tanstack/react-router";

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

  function logout() {
    clearAuth();
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
          <Button variant="outline" className="w-full" onClick={logout}>
            <LogOut className="size-4" /> Salir
          </Button>
        </div>
      </aside>

      {/* Header mobile */}
      <header className="flex items-center justify-between border-b bg-background px-4 py-3 md:hidden">
        <Link to="/" className="font-semibold">
          {title}
        </Link>
        <Sheet open={open} onOpenChange={setOpen}>
          <SheetTrigger asChild>
            <Button variant="ghost" size="icon">
              <Menu className="size-5" />
            </Button>
          </SheetTrigger>
          <SheetContent side="left" className="w-64 p-4">
            <p className="mb-6 text-lg font-semibold">{title}</p>
            {nav}
            <div className="mt-6">
              <Button variant="outline" className="w-full" onClick={logout}>
                <LogOut className="size-4" /> Salir
              </Button>
            </div>
          </SheetContent>
        </Sheet>
      </header>

      <main className="flex-1 p-4 md:p-8">
        <Outlet />
      </main>
    </div>
  );
}
