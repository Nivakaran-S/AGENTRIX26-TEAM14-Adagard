"use client";
// Super-Admin form to provision a new officer. Owner: Person C.
import { useActionState } from "react";
import { createOfficer } from "@/app/actions";

const ROLES = [
  { value: "REGISTRAR", label: "Registrar (birth/death)" },
  { value: "DRP_OFFICER", label: "DRP Officer (NIC)" },
  { value: "IMMIGRATION_OFFICER", label: "Immigration Officer (passport)" },
  { value: "GRAMA_NILADHARI", label: "Grama Niladhari (GN cert)" },
  { value: "DMT_EXAMINER", label: "DMT Examiner (licence)" },
];

const field =
  "w-full rounded-lg border border-line bg-paper/40 px-3 py-2 text-sm outline-none transition-colors focus:border-garnet focus:bg-card";

export default function CreateOfficerForm() {
  const [state, action, pending] = useActionState(createOfficer, null);

  return (
    <form action={action} className="overflow-hidden rounded-2xl border border-line bg-card shadow-sm">
      <div className="rule-saffron h-[2px] w-full" />
      <div className="grid gap-3 p-5 sm:grid-cols-2">
        <h2 className="font-display text-lg font-semibold tracking-tight sm:col-span-2">Add officer</h2>
        <input name="nic" required placeholder="NIC" className={`${field} font-mono`} />
        <input name="full_name" required placeholder="Full name" className={field} />
        <input name="password" type="password" required placeholder="Temp password (min 6)" className={field} />
        <select name="role" required defaultValue="REGISTRAR" className={field}>
          {ROLES.map((r) => (
            <option key={r.value} value={r.value}>
              {r.label}
            </option>
          ))}
        </select>
        <select name="jurisdiction" defaultValue="" className={`${field} sm:col-span-2`}>
          <option value="">Jurisdiction — all offices (non-registrar)</option>
          <option value="Divisional Secretariat">Divisional Secretariat (DS)</option>
          <option value="District Secretariat (Kachcheri)">District Secretariat (Kachcheri)</option>
        </select>

        <div className="flex items-center gap-3 sm:col-span-2">
          <button
            type="submit"
            disabled={pending}
            className="rounded-lg bg-garnet px-4 py-2 text-sm font-semibold text-paper transition-colors hover:bg-garnet-700 disabled:opacity-60"
          >
            {pending ? "Creating…" : "Create officer"}
          </button>
          {state?.error && <span className="text-sm text-garnet">{state.error}</span>}
          {state?.ok && <span className="text-sm text-palm">Officer created.</span>}
        </div>
      </div>
    </form>
  );
}
