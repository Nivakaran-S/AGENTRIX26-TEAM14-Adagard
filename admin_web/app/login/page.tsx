"use client";
// Officer login (NIC + password). Owner: Person C.
import { useActionState } from "react";
import { login } from "@/app/actions";
import { Wordmark } from "@/components/Seal";

export default function LoginPage() {
  const [state, action, pending] = useActionState(login, null);

  return (
    <main className="flex min-h-screen items-center justify-center bg-paper p-6">
      <form
        action={action}
        className="w-full max-w-sm overflow-hidden rounded-2xl border border-line bg-card shadow-[0_1px_0_rgba(33,26,36,0.04),0_18px_40px_-24px_rgba(122,22,49,0.35)]"
      >
        <div className="rule-saffron h-[3px] w-full" />
        <div className="space-y-6 p-8">
          <div className="space-y-3">
            <Wordmark />
            <div>
              <p className="font-mono text-[11px] uppercase tracking-[0.18em] text-saffron">
                Officer Portal
              </p>
              <h1 className="mt-1 font-display text-2xl font-semibold tracking-tight">
                Sign in to review
              </h1>
            </div>
          </div>

          <label className="block space-y-1.5">
            <span className="font-mono text-[11px] uppercase tracking-[0.12em] text-muted">NIC</span>
            <input
              name="nic"
              required
              autoComplete="username"
              placeholder="700000000001"
              className="w-full rounded-lg border border-line bg-paper/40 px-3 py-2.5 font-mono text-sm outline-none transition-colors focus:border-garnet focus:bg-card"
            />
          </label>

          <label className="block space-y-1.5">
            <span className="font-mono text-[11px] uppercase tracking-[0.12em] text-muted">Password</span>
            <input
              name="password"
              type="password"
              required
              autoComplete="current-password"
              className="w-full rounded-lg border border-line bg-paper/40 px-3 py-2.5 text-sm outline-none transition-colors focus:border-garnet focus:bg-card"
            />
          </label>

          {state?.error && (
            <p className="rounded-lg border border-garnet/20 bg-garnet/5 px-3 py-2 text-sm text-garnet">
              {state.error}
            </p>
          )}

          <button
            type="submit"
            disabled={pending}
            className="w-full rounded-lg bg-garnet px-4 py-2.5 text-sm font-semibold text-paper transition-colors hover:bg-garnet-700 disabled:opacity-60"
          >
            {pending ? "Signing in…" : "Sign in"}
          </button>
        </div>
      </form>
    </main>
  );
}
