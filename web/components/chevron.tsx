const PATHS = {
  left: "M10 3.5 5.5 8 10 12.5",
  right: "M6 3.5 10.5 8 6 12.5",
} as const;

/** Decorative only: the control it sits in must carry its own accessible name. */
export function Chevron({
  direction,
  className = "",
}: {
  direction: keyof typeof PATHS;
  className?: string;
}) {
  return (
    <svg
      viewBox="0 0 16 16"
      width={16}
      height={16}
      fill="none"
      stroke="currentColor"
      strokeWidth={1.5}
      strokeLinecap="round"
      strokeLinejoin="round"
      aria-hidden
      className={`shrink-0 ${className}`}
    >
      <path d={PATHS[direction]} />
    </svg>
  );
}
