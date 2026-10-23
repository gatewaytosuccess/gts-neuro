const CHOICES = [
  {
    persona: "learner",
    label: "Try as learner",
    hint: "Enrolled in two courses, partway through one. Watch, read and mark lessons complete.",
  },
  {
    persona: "admin",
    label: "Try as admin",
    hint: "Edit courses and lessons, browse orders and users. Some actions are turned off.",
  },
] as const;

export function PersonaChoice() {
  return (
    <ul className="flex flex-col gap-lg">
      {CHOICES.map((choice) => (
        <li key={choice.persona}>
          {/* Not <Link>: a prefetch would mint a sign-in token. */}
          <a href={`/demo/${choice.persona}`} className="button-primary">
            {choice.label}
          </a>
          <p className="type-body-sm measure mt-xs text-meta-text">
            {choice.hint}
          </p>
        </li>
      ))}
    </ul>
  );
}
