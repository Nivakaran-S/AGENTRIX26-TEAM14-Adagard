// Super-Admin officer management. Owner: Person C.
// Double-gated: backend rejects non-super-admins (403), and this page redirects them.
import { redirect } from "next/navigation";
import { getMe, apiFetch, type Me } from "@/lib/api";
import { setOfficerActive } from "@/app/actions";
import Header from "@/components/Header";
import CreateOfficerForm from "@/components/CreateOfficerForm";

export default async function OfficersPage() {
  const me = await getMe();
  if (!me) redirect("/login");
  if (!me.can_manage_users) redirect("/");

  const res = await apiFetch("/auth/officers");
  const officers: Me[] = res.ok ? await res.json() : [];

  return (
    <div className="min-h-screen bg-paper">
      <Header me={me} />
      <main className="mx-auto max-w-4xl space-y-6 px-6 py-8">
        <h1 className="font-display text-2xl font-semibold tracking-tight">Officers</h1>

        <CreateOfficerForm />

        <div className="overflow-hidden rounded-2xl border border-line bg-card shadow-sm">
          <table className="w-full text-left text-sm">
            <thead className="border-b border-line bg-paper/60">
              <tr className="font-mono text-[10px] uppercase tracking-[0.12em] text-muted">
                <th className="px-4 py-2.5 font-medium">Officer</th>
                <th className="px-4 py-2.5 font-medium">Role</th>
                <th className="px-4 py-2.5 font-medium">Scope</th>
                <th className="px-4 py-2.5 font-medium">Status</th>
                <th className="px-4 py-2.5"></th>
              </tr>
            </thead>
            <tbody>
              {officers.map((o) => {
                const active = o.is_active;
                const scope =
                  o.role === "SUPER_ADMIN"
                    ? "all services"
                    : `${o.services.join(" · ")}${o.jurisdiction ? ` — ${o.jurisdiction}` : ""}`;
                return (
                  <tr key={o.id} className="border-t border-line first:border-t-0">
                    <td className="px-4 py-3">
                      <div className="font-medium">{o.full_name}</div>
                      <div className="font-mono text-[11px] text-muted">{o.nic}</div>
                    </td>
                    <td className="px-4 py-3">
                      <span className="font-mono text-[11px] uppercase tracking-wide text-garnet">{o.role}</span>
                    </td>
                    <td className="px-4 py-3 text-muted">{scope}</td>
                    <td className="px-4 py-3">
                      {o.can_manage_users ? (
                        <span className="text-muted">—</span>
                      ) : (
                        <span
                          className={`inline-flex items-center gap-1.5 rounded-full px-2 py-0.5 text-[11px] font-medium ${
                            active ? "bg-palm-soft text-palm" : "bg-line/60 text-muted"
                          }`}
                        >
                          <span className={`h-1.5 w-1.5 rounded-full ${active ? "bg-palm" : "bg-muted"}`} />
                          {active ? "Active" : "Disabled"}
                        </span>
                      )}
                    </td>
                    <td className="px-4 py-3 text-right">
                      {!o.can_manage_users && (
                        <form action={setOfficerActive}>
                          <input type="hidden" name="id" value={o.id} />
                          <input type="hidden" name="is_active" value={active ? "false" : "true"} />
                          <button className="rounded-md border border-line px-2.5 py-1 text-xs transition-colors hover:border-garnet hover:text-garnet">
                            {active ? "Deactivate" : "Reactivate"}
                          </button>
                        </form>
                      )}
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      </main>
    </div>
  );
}
