import type { Metadata } from "next";
import Link from "next/link";
import type { ReactNode } from "react";

import { InfoPage } from "../_components/info-page";

export const metadata: Metadata = { title: "FAQ" };

const linkClass = "text-primary underline hover:text-primary-strong";

const questions: { question: string; answer: ReactNode }[] = [
  {
    question: "Can I try a course before I buy it?",
    answer:
      "Yes. Most courses have free preview lessons, marked in the curriculum on the course page. You can open them without an account.",
  },
  {
    question: "How do I buy a course?",
    answer:
      "Choose Buy now on the course page. Payment goes through Stripe, and you can start the course as soon as it’s confirmed.",
  },
  {
    question: "Does my progress carry across devices?",
    answer:
      "Yes. Completed lessons and where you stopped in a video are saved to your account, so you can pick up on any device.",
  },
  {
    question: "Where are my receipts?",
    answer: (
      <>
        Under{" "}
        <Link href="/account/orders" className={linkClass}>
          Order history
        </Link>{" "}
        in your account. Each order links to its Stripe receipt.
      </>
    ),
  },
  {
    question: "What if I delete my sign-in?",
    answer:
      "Your purchases are kept. Sign up again with the same email address and they come back.",
  },
  {
    question: "Can I get a refund?",
    answer: (
      <>
        See the{" "}
        <Link href="/refund-policy" className={linkClass}>
          refund policy
        </Link>
        , or{" "}
        <Link href="/contact" className={linkClass}>
          get in touch
        </Link>
        .
      </>
    ),
  },
];

export default function FaqPage() {
  return (
    <InfoPage eyebrow="FAQ" title="Questions, answered.">
      <dl className="measure border-b border-rule">
        {questions.map(({ question, answer }) => (
          <div key={question} className="border-t border-rule py-md">
            <dt className="type-label-lg">{question}</dt>
            <dd className="type-body-md mt-xs">{answer}</dd>
          </div>
        ))}
      </dl>
    </InfoPage>
  );
}
