import { redirect } from "next/navigation";

// The demo has only its two shared accounts.
export default function SignUpPage() {
  redirect("/sign-in");
}
