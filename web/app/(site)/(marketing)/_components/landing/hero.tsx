import Link from "next/link";
import { Show } from "@clerk/nextjs";

import { PERSONAS } from "@/lib/demo";

import type { HeroContent } from "./types";

export function Hero({ content }: { content: HeroContent }) {
  return (
    <section className="mx-auto max-w-[1200px] px-md py-2xl sm:px-margin lg:py-3xl">
      <p className="type-label-caps text-accent">{content.eyebrow}</p>
      <h1 className="type-headline-md measure mt-md lg:type-headline-lg">
        {content.headline}
      </h1>
      <p className="type-body-lg measure mt-lg">{content.body}</p>

      <div className="mt-xl flex flex-wrap gap-md">
        <Show
          when="signed-in"
          fallback={
            <>
              {PERSONAS.map((persona, index) => (
                // Not <Link>: a prefetch would mint a sign-in token.
                <a
                  key={persona}
                  href={`/demo/${persona}`}
                  className={
                    index === 0 ? "button-primary" : "button-secondary"
                  }
                >
                  Try as {persona}
                </a>
              ))}
            </>
          }
        >
          <Link href="/dashboard" className="button-primary">
            Go to your dashboard
          </Link>
        </Show>
      </div>
    </section>
  );
}
