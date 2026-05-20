import { useEffect, useState } from "react";
import type { User } from "@/lib/types";
import { getUser, getToken } from "@/lib/auth";

export function useAuth() {
  const [user, setUser] = useState<User | null>(null);
  const [token, setTokenState] = useState<string | null>(null);
  const [hydrated, setHydrated] = useState(false);

  useEffect(() => {
    const sync = () => {
      setUser(getUser());
      setTokenState(getToken());
    };
    sync();
    setHydrated(true);
    window.addEventListener("auth-change", sync);
    window.addEventListener("storage", sync);
    return () => {
      window.removeEventListener("auth-change", sync);
      window.removeEventListener("storage", sync);
    };
  }, []);

  return { user, token, hydrated, isAuthenticated: !!token };
}
