// Stands in for an action the demo's API refuses.
export function DemoDisabled({ className = "" }: { className?: string }) {
  return (
    <p
      className={`type-label-caps inline-block rounded-xs border border-dashed border-warning bg-warning-subtle px-xs py-[2px] text-warning ${className}`}
    >
      Disabled in the demo
    </p>
  );
}
