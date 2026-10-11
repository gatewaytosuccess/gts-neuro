"use client";

import { useActionState, useId } from "react";

import { formatPrice } from "@/lib/format";

import { Modal, useDialog } from "../../users/_components/dialog";
import type { RefundState } from "../_lib/refund";

type RefundAction = (
  state: RefundState,
  formData: FormData,
) => Promise<RefundState>;

const dangerClassName =
  "type-label-md rounded-sm border border-error bg-paper-raised px-sm py-xs text-error hover:bg-error-subtle";

export function RefundDialog({
  amountCents,
  buyerName,
  refund,
}: {
  /** What remains to refund. */
  amountCents: number;
  buyerName: string;
  refund: RefundAction;
}) {
  const { dialogRef, opened, open, close } = useDialog();
  const headingId = useId();

  return (
    <div className="mt-lg">
      <button type="button" onClick={open} className={dangerClassName}>
        Refund…
      </button>
      <Modal dialogRef={dialogRef} headingId={headingId}>
        {/* Keyed by opening, so a reopened dialog starts blank. */}
        <RefundForm
          key={opened}
          amountCents={amountCents}
          buyerName={buyerName}
          headingId={headingId}
          refund={refund}
          onCancel={close}
        />
      </Modal>
    </div>
  );
}

function RefundForm({
  amountCents,
  buyerName,
  headingId,
  refund,
  onCancel,
}: {
  amountCents: number;
  buyerName: string;
  headingId: string;
  refund: RefundAction;
  onCancel: () => void;
}) {
  const [state, formAction, pending] = useActionState(refund, {});
  const fieldId = useId();
  const hintId = `${fieldId}-hint`;
  const errorId = `${fieldId}-error`;
  const amount = formatPrice(amountCents);

  return (
    // The reason reads its default from `state`: React resets the form after every submission.
    <form action={formAction} className="flex flex-col gap-md">
      <h2 id={headingId} className="type-headline-sm break-words">
        Refund {amount} to {buyerName}?
      </h2>
      <p className="type-body-md">
        Stripe sends {amount} back to them and the order becomes Refunded. Their
        access to its courses is kept; revoke it on their page if needed.
      </p>
      <div>
        <label htmlFor={fieldId} className="type-label-md block">
          Reason
        </label>
        <textarea
          id={fieldId}
          name="reason"
          rows={4}
          required
          maxLength={500}
          defaultValue={state.reason}
          aria-describedby={
            state.reasonErrors ? `${hintId} ${errorId}` : hintId
          }
          {...(state.reasonErrors && { "aria-invalid": true })}
          className={`type-body-md mt-xs w-full rounded-sm border bg-paper-raised px-sm py-sm text-accent-strong ${
            state.reasonErrors ? "border-error" : "border-border-strong"
          }`}
        />
        <p id={hintId} className="type-caption mt-xs text-meta-text">
          Only admins see this. Up to 500 characters.
        </p>
        {state.reasonErrors && (
          <p id={errorId} className="type-body-sm mt-xs text-error">
            {state.reasonErrors.join(" ")}
          </p>
        )}
      </div>
      {state.error && (
        <p
          role="alert"
          className="type-body-sm rounded-sm bg-error-subtle px-sm py-xs text-error"
        >
          {state.error}
        </p>
      )}
      <div className="flex flex-wrap gap-md">
        <button
          type="submit"
          disabled={pending}
          className={`${dangerClassName} disabled:cursor-wait disabled:opacity-60`}
        >
          {pending ? "Refunding…" : `Refund ${amount}`}
        </button>
        <button type="button" onClick={onCancel} className="button-secondary">
          Cancel
        </button>
      </div>
    </form>
  );
}
