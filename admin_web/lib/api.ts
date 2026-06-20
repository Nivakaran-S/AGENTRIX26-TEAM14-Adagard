// Server-only helpers for talking to the GovPath backend with the officer's JWT.
// Owner: Person C. The token lives in an httpOnly cookie (set in app/actions.ts).
import { cookies } from "next/headers";

export const BACKEND_URL = process.env.BACKEND_URL ?? "http://localhost:8000";
export const TOKEN_COOKIE = "govpath_token";

export type Me = {
  id: number;
  kind: string;
  nic: string;
  full_name: string;
  role: string;
  services: string[];
  jurisdiction: string | null;
  is_active: boolean;
  can_manage_users: boolean;
};

export type Plan = {
  office: string;
  officer: string;
  checklist: string[];
  forms: { name: string; url: string }[];
  draft_docs: { type: string; content: string }[];
  citations: { title: string; source: string }[];
};

export type Packet = {
  id: string;
  session_id: string;
  service: string;
  plan: Plan;
  approved: boolean;
  officer: string | null;
};

export async function getToken(): Promise<string | undefined> {
  const store = await cookies();
  return store.get(TOKEN_COOKIE)?.value;
}

/** Authenticated fetch to the backend; attaches Bearer + JSON headers. */
export async function apiFetch(path: string, init: RequestInit = {}): Promise<Response> {
  const token = await getToken();
  const headers = new Headers(init.headers);
  if (token) headers.set("Authorization", `Bearer ${token}`);
  if (init.body && !headers.has("Content-Type")) headers.set("Content-Type", "application/json");
  return fetch(`${BACKEND_URL}${path}`, { ...init, headers, cache: "no-store" });
}

export async function getMe(): Promise<Me | null> {
  const res = await apiFetch("/auth/me");
  return res.ok ? ((await res.json()) as Me) : null;
}
