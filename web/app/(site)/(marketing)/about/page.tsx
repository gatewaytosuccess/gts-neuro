import type { Metadata } from "next";
import Link from "next/link";

import { PlaceholderBadge } from "../_components/landing/placeholder-badge";
import { InfoPage } from "../_components/info-page";
import { landing } from "../_content/landing";

export const metadata: Metadata = { title: "About" };

export default function AboutPage() {
  const { instructor } = landing;

  return (
    <InfoPage eyebrow="About the instructor" title={instructor.name}>
      <p className="type-caption text-meta-text">{instructor.title}</p>
      <div className="mt-sm">
        <PlaceholderBadge show={instructor.placeholder} />
      </div>

      {instructor.bio.map((paragraph) => (
        <p key={paragraph} className="type-body-lg measure mt-md">
          {paragraph}
        </p>
      ))}

      <h2 className="type-label-caps mt-xl text-accent">Credentials</h2>
      <ul className="measure mt-sm border-b border-rule">
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
        <Link href="/courses" className="button-primary">
          Browse the courses
        </Link>
      </div>
    </InfoPage>
  );
}
