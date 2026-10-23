import type { Metadata } from "next";
import { redirect } from "next/navigation";

import { isPersona } from "@/lib/demo";

import { TicketSignIn } from "./_components/ticket-sign-in";

export const metadata: Metadata = {
  title: "Signing in",
  robots: { index: false, follow: false },
};

export default async function DemoSignInPage({
  searchParams,
}: PageProps<"/demo/sign-in">) {
  const { persona, ticket } = await searchParams;
  if (!isPersona(persona) || typeof ticket !== "string") redirect("/sign-in");

  return (
    <main className="mx-auto w-full max-w-[1200px] flex-1 px-md py-3xl sm:px-margin">
      <TicketSignIn persona={persona} ticket={ticket} />
    </main>
  );
}
