import type { Metadata } from "next";

import { AuthSplitPanel } from "@/components/auth-split-panel";
import { PersonaChoice } from "@/components/persona-choice";

export const metadata: Metadata = {
  title: "Sign in",
};

// The demo accounts have no passwords; they sign in with a one-time token.
export default function SignInPage() {
  return (
    <AuthSplitPanel eyebrow="Demo" headline="Choose how to look around">
      <PersonaChoice />
    </AuthSplitPanel>
  );
}
