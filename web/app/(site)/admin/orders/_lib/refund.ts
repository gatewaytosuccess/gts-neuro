/** What the refund dialog shows after submitting. */
export type RefundState = {
  /** The reason as typed, so a refused submission keeps it. */
  reason?: string;
  reasonErrors?: string[];
  error?: string;
};

export const BLANK_REASON_ERROR = "Give a reason for refunding this order.";
