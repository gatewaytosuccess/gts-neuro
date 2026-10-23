import { auth, clerkClient } from "@clerk/nextjs/server";
import { notFound } from "next/navigation";
import { NextResponse, type NextRequest } from "next/server";

import { isPersona, PERSONA_HOME, personaUserIds } from "@/lib/demo";

/**
 * `/demo/learner` and `/demo/admin`: one-click sign-in to a shared demo
 * account. Link with a plain `<a>`: a prefetch would mint a sign-in token.
 */
export async function GET(
  request: NextRequest,
  { params }: RouteContext<"/demo/[persona]">,
) {
  const { persona } = await params;
  if (!isPersona(persona)) notFound();

  const { userId } = await auth();
  if (userId) {
    return NextResponse.redirect(
      new URL(PERSONA_HOME[persona], request.url),
      303,
    );
  }

  const clerkUserId = personaUserIds()[persona];
  if (!clerkUserId) notFound();

  const { token } = await (
    await clerkClient()
  ).signInTokens.createSignInToken({
    userId: clerkUserId,
    expiresInSeconds: 60,
  });
  const destination = new URL("/demo/sign-in", request.url);
  destination.searchParams.set("persona", persona);
  destination.searchParams.set("ticket", token);
  return NextResponse.redirect(destination, 303);
}
