import Link from "next/link";

import { InfoPage } from "./info-page";

export function PolicyPending({ title }: { title: string }) {
  return (
    <InfoPage eyebrow="Legal" title={title}>
      <p className="type-body-lg measure text-accent-strong">
        This policy is being drafted and will be published here before courses
        go on sale.
      </p>
      <p className="type-body-md measure mt-md">
        Questions in the meantime?{" "}
        <Link
          href="/contact"
          className="text-primary underline hover:text-primary-strong"
        >
          Get in touch
        </Link>
        .
      </p>
    </InfoPage>
  );
}
