import Link from "next/link";
import type { ReactNode } from "react";

import { Chevron } from "@/components/chevron";

/** A crumb without `href` is the current page. */
export type Crumb = { label: ReactNode; href?: string };

export function Breadcrumbs({ items }: { items: Crumb[] }) {
  return (
    <nav aria-label="Breadcrumb">
      <ol className="type-label-md flex flex-wrap items-center gap-xs">
        {items.map((item, index) => (
          <li key={index} className="flex min-w-0 items-center gap-xs">
            {item.href ? (
              <Link href={item.href} className="text-primary hover:underline">
                {item.label}
              </Link>
            ) : (
              <span
                aria-current="page"
                className="min-w-0 break-words text-meta-text"
              >
                {item.label}
              </span>
            )}
            {index < items.length - 1 && (
              <Chevron
                direction="right"
                className="size-3 text-border-strong"
              />
            )}
          </li>
        ))}
      </ol>
    </nav>
  );
}
