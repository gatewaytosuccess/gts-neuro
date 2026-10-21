import type { Metadata } from "next";

import { PolicyPending } from "../_components/policy-pending";

export const metadata: Metadata = { title: "Terms of Service" };

export default function TermsPage() {
  return <PolicyPending title="Terms of Service" />;
}
