import Link from "next/link";

import type { CourseSummary } from "@/lib/api";
import { formatPrice } from "@/lib/format";
import { markdownExcerpt } from "@/lib/markdown-excerpt";

export function CourseCard({
  course,
  heading: Heading,
  enrolled = false,
}: {
  course: CourseSummary;
  heading: "h2" | "h3";
  enrolled?: boolean;
}) {
  return (
    <Link
      href={`/courses/${course.slug}`}
      className="group flex h-full flex-col rounded-lg border border-rule bg-paper-raised p-lg transition-[box-shadow,translate,border-color] duration-100 hover:-translate-y-0.5 hover:border-border-strong/60 hover:shadow-lift motion-reduce:transition-none motion-reduce:hover:translate-y-0"
    >
      {course.thumbnail_url ? (
        // CloudFront's domain is a Django setting, so next/image has no host to allowlist.
        // eslint-disable-next-line @next/next/no-img-element
        <img
          src={course.thumbnail_url}
          alt=""
          className="h-[220px] w-full rounded-xs bg-paper-dim object-cover"
        />
      ) : (
        <div aria-hidden className="h-[220px] rounded-xs bg-paper-dim" />
      )}

      <Heading className="type-headline-sm mt-md group-hover:text-primary">
        {course.title}
      </Heading>
      <p className="type-body-md mt-sm line-clamp-3">
        {markdownExcerpt(course.description)}
      </p>
      <Rating average={course.rating_average} count={course.rating_count} />

      <div className="mt-auto pt-lg">
        <div className="border-t border-rule pt-md">
          {enrolled ? (
            <span className="type-label-md text-tertiary-strong">Enrolled</span>
          ) : (
            <span className="type-data-md">
              {formatPrice(course.price_cents)}
            </span>
          )}
        </div>
      </div>
    </Link>
  );
}

function Rating({ average, count }: { average: number | null; count: number }) {
  if (average === null || count === 0) {
    return <p className="type-caption mt-sm text-meta-text">No ratings yet</p>;
  }

  return (
    <p className="type-data-md mt-sm text-meta-text">
      <span aria-hidden className="text-tertiary-strong">
        ★{" "}
      </span>
      <span className="sr-only">Rated </span>
      {average.toFixed(1)}
      <span className="type-caption">
        {" "}
        ({count.toLocaleString("en-US")}
        <span className="sr-only"> ratings</span>)
      </span>
    </p>
  );
}
