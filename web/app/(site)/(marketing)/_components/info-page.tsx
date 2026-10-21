import type { ReactNode } from "react";

export function InfoPage({
  eyebrow,
  title,
  children,
}: {
  eyebrow: string;
  title: string;
  children: ReactNode;
}) {
  return (
    <div className="mx-auto max-w-[1200px] px-md py-2xl sm:px-margin lg:py-3xl">
      <p className="type-label-caps text-accent">{eyebrow}</p>
      <h1 className="type-headline-md measure mt-md lg:type-headline-lg">
        {title}
      </h1>
      <div className="mt-lg">{children}</div>
    </div>
  );
}
