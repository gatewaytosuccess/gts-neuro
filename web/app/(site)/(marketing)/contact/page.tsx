import type { Metadata } from "next";

import { InfoPage } from "../_components/info-page";

export const metadata: Metadata = { title: "Contact" };

export default function ContactPage() {
  const email = process.env.CONTACT_EMAIL;

  return (
    <InfoPage eyebrow="Contact" title="Get in touch.">
      <p className="type-body-lg measure text-accent-strong">
        Questions about a course, your account or an order? Write to us and
        we&rsquo;ll get back to you.
      </p>
      {email ? (
        <a href={`mailto:${email}`} className="button-primary mt-xl">
          {email}
        </a>
      ) : (
        <p className="type-body-md measure mt-md text-meta-text">
          A contact address will be published here before courses go on sale.
        </p>
      )}
    </InfoPage>
  );
}
