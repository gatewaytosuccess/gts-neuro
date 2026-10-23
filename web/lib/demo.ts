export const PERSONAS = ["learner", "admin"] as const;

export type Persona = (typeof PERSONAS)[number];

export const PERSONA_HOME: Record<Persona, string> = {
  learner: "/dashboard",
  admin: "/admin",
};

export function isPersona(value: unknown): value is Persona {
  return PERSONAS.includes(value as Persona);
}

/** Server-only: the Clerk user id of each shared demo account, blank if unset. */
export function personaUserIds(): Record<Persona, string> {
  return {
    learner: process.env.DEMO_LEARNER_CLERK_USER_ID ?? "",
    admin: process.env.DEMO_ADMIN_CLERK_USER_ID ?? "",
  };
}

/** Server-only: lowercased emails of the shared demo accounts. */
export function demoAccountEmails(): string[] {
  return (process.env.DEMO_ACCOUNT_EMAILS ?? "")
    .split(",")
    .map((email) => email.trim().toLowerCase())
    .filter(Boolean);
}

export function isDemoAccount(email: string) {
  return demoAccountEmails().includes(email.toLowerCase());
}
