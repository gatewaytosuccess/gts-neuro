import Link from "next/link";

import { PlaceholderBadge } from "./placeholder-badge";
import type { Instructor } from "./types";

export function InstructorCredentials({
  instructor,
}: {
  instructor: Instructor;
}) {
  return (
    <section aria-labelledby="instructor-heading" className="bg-paper-dim">
      <div className="mx-auto grid max-w-[1200px] gap-xl px-md py-2xl sm:px-margin md:grid-cols-12 md:gap-gutter lg:py-3xl">
        {/* Monogram until a real photo exists. */}
        <div
          aria-hidden
          className="flex aspect-[4/5] w-full max-w-[360px] items-center justify-center rounded-xs bg-primary md:col-span-4"
        >
          <span className="type-display text-primary-pale">
            {instructor.initials}
          </span>
        </div>

        <div className="md:col-span-8 lg:col-span-7 lg:col-start-6">
          <p className="type-label-caps text-accent">Your instructor</p>
          <h2
            id="instructor-heading"
            className="type-headline-sm mt-sm lg:type-headline-md"
          >
            {instructor.name}
          </h2>
          <p className="type-caption mt-xs text-meta-text">
            {instructor.title}
          </p>
          <div className="mt-sm">
            <PlaceholderBadge show={instructor.placeholder} />
          </div>

          <p className="type-body-lg measure mt-md">{instructor.summary}</p>

          <ul className="measure mt-lg border-b border-rule">
            {instructor.credentials.map((credential) => (
              <li
                key={credential}
                className="type-body-md border-t border-rule py-sm"
              >
                {credential}
              </li>
            ))}
          </ul>

          <div className="mt-xl">
            <Link href="/about" className="button-secondary">
              Read more
            </Link>
          </div>
        </div>
      </div>
    </section>
  );
}
