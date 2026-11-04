"use client";

import { useAuth } from "@clerk/nextjs";
import { usePathname } from "next/navigation";
import { useEffect, useId, useRef } from "react";

import { Modal } from "@/components/dialog";
import { PERSONA_CHOICES } from "@/components/persona-choice";

const SEEN_KEY = "demo-intro-seen";

/** Opens once per tab session, on the landing page, for signed-out visitors. */
export function DemoIntro() {
  const pathname = usePathname();
  const { isLoaded, userId } = useAuth();
  const dialogRef = useRef<HTMLDialogElement>(null);
  const headingId = useId();

  useEffect(() => {
    const dialog = dialogRef.current;
    if (!dialog || dialog.open) return;
    if (pathname !== "/" || !isLoaded || userId) return;

    try {
      if (sessionStorage.getItem(SEEN_KEY)) return;
      sessionStorage.setItem(SEEN_KEY, "1");
    } catch {
      // Storage blocked: show it on every visit rather than never.
    }
    dialog.showModal();
  }, [pathname, isLoaded, userId]);

  useEffect(() => {
    const dialog = dialogRef.current;
    if (!dialog) return;
    // Backdrop clicks target the dialog itself, so this covers inside and out.
    const close = () => dialog.close();
    dialog.addEventListener("click", close);
    return () => dialog.removeEventListener("click", close);
  }, []);

  return (
    <Modal dialogRef={dialogRef} headingId={headingId}>
      <div className="flex flex-col gap-md">
        <h2 id={headingId} className="type-headline-sm">
          This is a demo
        </h2>
        <p className="type-body-md">
          Everything here is sample data, reset every night.
        </p>
        <dl className="flex flex-col gap-sm">
          {PERSONA_CHOICES.map((choice) => (
            <div key={choice.persona}>
              <dt className="type-label-md">{choice.label}</dt>
              <dd className="type-body-md">{choice.hint}</dd>
            </div>
          ))}
        </dl>
        <p className="type-body-md">
          There&rsquo;s no real checkout; nothing is charged.
        </p>
        <p className="type-body-sm text-meta-text">
          Click anywhere to continue.
        </p>
      </div>
    </Modal>
  );
}
