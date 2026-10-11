"use server";

import { refresh } from "next/cache";

import { ApiError, refundAdminOrder, type FieldErrors } from "@/lib/api";

import { BLANK_REASON_ERROR, type RefundState } from "./refund";

function errorState(error: unknown): RefundState {
  if (!(error instanceof ApiError)) {
    return { error: "The course API is not responding, so nothing changed." };
  }
  const detail =
    typeof error.body === "object" && error.body && "detail" in error.body
      ? String(error.body.detail)
      : undefined;
  if (error.status === 400 && typeof error.body === "object" && error.body) {
    const { reason, non_field_errors } = error.body as FieldErrors;
    return { reasonErrors: reason, error: non_field_errors?.join(" ") };
  }
  if (error.status === 401 || error.status === 403) {
    return { error: "You no longer have access to the admin area." };
  }
  if (error.status === 404) {
    return { error: "This order no longer exists." };
  }
  if (error.status === 409) {
    return { error: detail ?? "This order can no longer be refunded." };
  }
  if (error.status === 502) {
    return {
      error: detail
        ? `Stripe refused the refund: ${detail}`
        : "Stripe refused the refund.",
    };
  }
  return { error: "The course API couldn't refund this order. Try again." };
}

export async function refundOrder(
  id: string,
  _previous: RefundState,
  formData: FormData,
): Promise<RefundState> {
  const reason = String(formData.get("reason") ?? "").trim();
  if (!reason) return { reason, reasonErrors: [BLANK_REASON_ERROR] };

  try {
    await refundAdminOrder(id, reason);
  } catch (error) {
    return { reason, ...errorState(error) };
  }
  refresh();
  return {};
}
