import type { Metadata } from "next";

import { PolicyPending } from "../_components/policy-pending";

export const metadata: Metadata = { title: "Refund Policy" };

export default function RefundPolicyPage() {
  return <PolicyPending title="Refund Policy" />;
}
