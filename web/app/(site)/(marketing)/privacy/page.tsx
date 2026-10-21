import type { Metadata } from "next";

import { PolicyPending } from "../_components/policy-pending";

export const metadata: Metadata = { title: "Privacy Policy" };

export default function PrivacyPage() {
  return <PolicyPending title="Privacy Policy" />;
}
