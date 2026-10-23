"use client";

import { useSignIn } from "@clerk/nextjs";
import { useRouter } from "next/navigation";
import { useEffect, useRef, useState } from "react";

import { PERSONA_HOME, type Persona } from "@/lib/demo";

export function TicketSignIn({
  persona,
  ticket,
}: {
  persona: Persona;
  ticket: string;
}) {
  const { signIn } = useSignIn();
  const router = useRouter();
  const [failed, setFailed] = useState(false);
  // A ticket works once, and Strict Mode runs effects twice.
  const started = useRef(false);

  useEffect(() => {
    if (started.current) return;
    started.current = true;

    (async () => {
      const { error } = await signIn.ticket({ ticket });
      if (error || signIn.status !== "complete") {
        setFailed(true);
        return;
      }
      const finalized = await signIn.finalize({
        navigate: ({ decorateUrl }) => {
          const url = decorateUrl(PERSONA_HOME[persona]);
          if (url.startsWith("http")) window.location.href = url;
          else router.push(url);
        },
      });
      if (finalized.error) setFailed(true);
    })();
  }, [signIn, ticket, persona, router]);

  if (failed) {
    return (
      <div role="alert">
        <h1 className="type-headline-md">
          That sign-in link didn&rsquo;t work.
        </h1>
        <p className="type-body-lg measure mt-md">
          Links expire after a minute. Start again to get a fresh one.
        </p>
        {/* Not <Link>: a prefetch would mint a sign-in token. */}
        <a href={`/demo/${persona}`} className="button-primary mt-xl">
          Try as {persona} again
        </a>
      </div>
    );
  }

  return (
    <p role="status" className="type-headline-sm">
      Signing you in as the demo {persona}&hellip;
    </p>
  );
}
