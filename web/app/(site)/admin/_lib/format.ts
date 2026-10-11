const dateFormat = new Intl.DateTimeFormat("en-US", {
  year: "numeric",
  month: "short",
  day: "numeric",
});

/** "Sep 30, 2026", from an ISO timestamp. */
export function formatDate(iso: string) {
  return dateFormat.format(new Date(iso));
}

const dateTimeFormat = new Intl.DateTimeFormat("en-US", {
  year: "numeric",
  month: "short",
  day: "numeric",
  hour: "numeric",
  minute: "2-digit",
  timeZoneName: "short",
});

/** "Sep 30, 2026, 4:05 PM PDT", from an ISO timestamp. */
export function formatDateTime(iso: string) {
  return dateTimeFormat.format(new Date(iso));
}
