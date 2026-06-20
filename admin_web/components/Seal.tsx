// GovPath seal — the brand mark. A garnet official seal with a saffron ring and a
// "path" notch (the right way through). Owner: Person C.
export default function Seal({ size = 28 }: { size?: number }) {
  return (
    <svg width={size} height={size} viewBox="0 0 40 40" fill="none" aria-hidden="true">
      <circle cx="20" cy="20" r="18.5" fill="#7a1631" />
      <circle cx="20" cy="20" r="16" fill="none" stroke="#e0a22b" strokeWidth="1.4" strokeDasharray="2 2.4" />
      {/* the path: a route winding upward to a marked destination */}
      <path
        d="M14 29c0-4 6-4 6-8s-5-4-5-8"
        fill="none"
        stroke="#faf5ec"
        strokeWidth="2.1"
        strokeLinecap="round"
      />
      <circle cx="26" cy="14" r="2.4" fill="#e0a22b" />
    </svg>
  );
}

export function Wordmark({ tag = "GovPath", size = 28 }: { tag?: string; size?: number }) {
  return (
    <span className="flex items-center gap-2">
      <Seal size={size} />
      <span className="font-display text-xl font-semibold tracking-tight text-garnet">{tag}</span>
    </span>
  );
}
