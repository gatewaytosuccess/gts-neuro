import type { Metadata } from "next";
import { auth } from "@clerk/nextjs/server";
import { redirect } from "next/navigation";

import { fetchCurrentUser, isAccountSuspended } from "@/lib/api";

import { AccountTabs } from "../_components/account-tabs";

export const metadata: Metadata = {
  title: "Account",
  robots: { index: false, follow: false },
};

export default async function AccountPage() {
  const { userId, redirectToSignIn } = await auth();
  if (!userId) return redirectToSignIn();

  // Any other failure still renders: Clerk's component doesn't need Django.
  try {
    await fetchCurrentUser();
  } catch (error) {
    if (isAccountSuspended(error)) redirect("/suspended");
  }

  return (
    <main className="mx-auto w-full max-w-[1200px] flex-1 px-md py-2xl sm:px-margin">
      <p className="type-label-caps text-accent">Your account</p>
      <h1 className="type-headline-md measure mt-md">Account settings</h1>
      <AccountTabs current="settings" />

      {/* Clerk's profile would let a visitor rename, re-email or delete a shared account. */}
      <p className="type-body-md measure mt-xl rounded-sm bg-warning-subtle px-sm py-sm text-warning">
        Account settings are turned off in this demo: everyone signs in to the
        same two accounts. Your order history is still here.
      </p>
    </main>
  );
}
