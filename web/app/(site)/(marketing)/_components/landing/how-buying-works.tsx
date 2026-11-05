import Link from "next/link";

import { SectionHeading } from "./section-heading";
import type { BuyingContent } from "./types";

export function HowBuyingWorks({ content }: { content: BuyingContent }) {
  return (
    <section
      aria-labelledby="buying-heading"
      className="mx-auto max-w-[1200px] px-md py-2xl sm:px-margin lg:py-3xl"
    >
      <SectionHeading
        id="buying-heading"
        eyebrow={content.eyebrow}
        title={content.title}
      />

      <ul className="mt-xl grid gap-gutter md:grid-cols-2">
        {content.items.map((item) => (
          <li key={item.title}>
            <h3 className="type-headline-sm">{item.title}</h3>
            <p className="type-body-md mt-sm">{item.body}</p>
          </li>
        ))}
      </ul>

      <div className="mt-xl">
        <Link href={content.cta.href} className="button-secondary">
          {content.cta.label}
        </Link>
      </div>
    </section>
  );
}
