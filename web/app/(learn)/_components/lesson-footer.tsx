import Link from "next/link";

import { Chevron } from "@/components/chevron";

import { CourseComplete } from "./course-complete";
import { MarkComplete } from "./mark-complete";

const linkClass = "button-secondary-dark gap-xs text-center";
// Icon-only below sm, so all three controls fit on one row.
const stepClass = `${linkClass} max-sm:px-sm`;
const stepLabelClass = "max-sm:sr-only";

export function LessonFooter({
  slug,
  lessonId,
  previousLessonId,
  nextLessonId,
}: {
  slug: string;
  lessonId: string;
  previousLessonId: string | null;
  nextLessonId: string | null;
}) {
  const lessonHref = (id: string) =>
    `/learn/${encodeURIComponent(slug)}/${encodeURIComponent(id)}`;

  return (
    <footer className="mt-2xl border-t border-dark-rule pt-lg">
      <div className="grid grid-cols-[1fr_auto_1fr] items-start gap-md">
        <span>
          {previousLessonId && (
            <Link href={lessonHref(previousLessonId)} className={stepClass}>
              <Chevron direction="left" />
              <span className={stepLabelClass}>Previous</span>
            </Link>
          )}
        </span>
        {/* Holds the middle column when there's no button. */}
        <span>
          <MarkComplete lessonId={lessonId} />
        </span>
        <span className="justify-self-end">
          {nextLessonId ? (
            <Link href={lessonHref(nextLessonId)} className={stepClass}>
              <span className={stepLabelClass}>Next</span>
              <Chevron direction="right" />
            </Link>
          ) : (
            <Link
              href={`/courses/${encodeURIComponent(slug)}`}
              className={linkClass}
            >
              Back to course
            </Link>
          )}
        </span>
      </div>
      {!nextLessonId && <CourseComplete slug={slug} />}
    </footer>
  );
}
