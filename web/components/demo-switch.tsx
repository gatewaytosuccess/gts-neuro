"use client";

import { useAuth, useClerk } from "@clerk/nextjs";

import { PERSONAS, type Persona } from "@/lib/demo";

export function DemoSwitch({
  userIds,
  dark,
}: {
  userIds: Record<Persona, string>;
  dark: boolean;
}) {
  const { isLoaded, userId } = useAuth();
  const { signOut } = useClerk();
  const buttonClassName = dark ? "button-secondary-dark" : "button-secondary";

  if (!isLoaded) return null;

  if (!userId) {
    return (
      <div className="flex flex-wrap gap-sm">
        {PERSONAS.map((persona) => (
          // Not <Link>: a prefetch would mint a sign-in token.
          <a
            key={persona}
            href={`/demo/${persona}`}
            className={buttonClassName}
          >
            Try as {persona}
          </a>
        ))}
      </div>
    );
  }

  const others = PERSONAS.filter((persona) => userIds[persona] !== userId);
  return (
    <div className="flex flex-wrap gap-sm">
      {others.map((persona) => (
        <button
          key={persona}
          type="button"
          onClick={() => signOut({ redirectUrl: `/demo/${persona}` })}
          className={buttonClassName}
        >
          Switch to {persona}
        </button>
      ))}
    </div>
  );
}
