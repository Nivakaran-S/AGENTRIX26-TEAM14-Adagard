"use client";
// Approve = an official stamp. Shows a brief "Stamping…" state while the server action
// authorizes and the packet leaves the queue. Owner: Person C.
import { useFormStatus } from "react-dom";

export default function ApproveButton() {
  const { pending } = useFormStatus();
  return (
    <button
      disabled={pending}
      className="stamp inline-flex items-center gap-2 rounded-lg border-2 border-garnet bg-garnet px-4 py-1.5 text-xs font-semibold uppercase text-paper transition-colors hover:bg-garnet-700 disabled:opacity-70"
    >
      <svg width="14" height="14" viewBox="0 0 24 24" fill="none" aria-hidden="true">
        <path d="M5 13l4 4L19 7" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round" />
      </svg>
      {pending ? "Stamping…" : "Approve"}
    </button>
  );
}
