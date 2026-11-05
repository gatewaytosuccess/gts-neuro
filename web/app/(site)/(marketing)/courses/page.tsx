import type { Metadata } from "next";
import Form from "next/form";
import Link from "next/link";

import { AutoSubmitSelect } from "@/components/auto-submit-select";
import { CourseCard } from "@/components/course-card";
import {
  fetchCourses,
  fetchEnrollments,
  isCourseSort,
  type CourseSort,
} from "@/lib/api";

export const metadata: Metadata = {
  title: "Courses",
};

const SORT_LABELS: Record<CourseSort, string> = {
  newest: "Newest",
  price_asc: "Price: low to high",
  price_desc: "Price: high to low",
};

type SearchParams = { [key: string]: string | string[] | undefined };

function firstValue(value: string | string[] | undefined): string {
  return (Array.isArray(value) ? value[0] : value) ?? "";
}

export default async function CoursesPage({
  searchParams,
}: {
  searchParams: Promise<SearchParams>;
}) {
  const params = await searchParams;
  const q = firstValue(params.q).trim();
  const requestedSort = firstValue(params.sort);
  const sort = isCourseSort(requestedSort) ? requestedSort : "newest";

  const [catalog, enrollments] = await Promise.allSettled([
    fetchCourses({ q, sort }),
    fetchEnrollments(),
  ]);

  // An unreachable API should degrade to a page that says so, not a 500.
  const courses = catalog.status === "fulfilled" ? catalog.value.results : null;

  // A failed enrollments call (suspended account, API error) shows no enrollment state.
  const enrolledCourseIds = new Set(
    enrollments.status === "fulfilled"
      ? (enrollments.value ?? []).map((enrollment) => enrollment.course_id)
      : [],
  );

  return (
    <div className="mx-auto max-w-[1200px] px-md py-2xl sm:px-margin lg:py-3xl">
      <p className="type-label-caps text-accent">The catalog</p>
      <h1 className="type-headline-md measure mt-md">Courses</h1>

      {courses !== null && (courses.length > 0 || q) && (
        <CatalogControls q={q} sort={sort} />
      )}

      <div className="mt-xl">
        {courses === null ? (
          <p className="type-body-sm rounded-sm bg-warning-subtle px-sm py-sm text-warning">
            The course API is not responding, so the catalog is unavailable.
          </p>
        ) : courses.length === 0 && q ? (
          <div className="measure">
            <p className="type-body-lg text-accent-strong">
              No courses match &ldquo;{q}&rdquo;.
            </p>
            <p className="type-body-md mt-sm">
              Try a different word, or{" "}
              <Link href="/courses" className="text-primary underline">
                browse every course
              </Link>
              .
            </p>
          </div>
        ) : courses.length === 0 ? (
          <p className="type-body-lg measure text-accent-strong">
            No courses are published yet. Check back soon.
          </p>
        ) : (
          <ul className="grid gap-gutter md:grid-cols-2 lg:grid-cols-3">
            {courses.map((course) => (
              <li key={course.id}>
                <CourseCard
                  course={course}
                  heading="h2"
                  enrolled={enrolledCourseIds.has(course.id)}
                />
              </li>
            ))}
          </ul>
        )}
      </div>
    </div>
  );
}

const fieldClassName =
  "type-body-md w-full rounded-sm border border-border-strong bg-paper-raised px-sm py-sm text-accent-strong placeholder:text-meta-text";

function CatalogControls({ q, sort }: { q: string; sort: CourseSort }) {
  return (
    // Remounts per URL: uncontrolled fields would keep stale values across client-side back/forward.
    <Form
      key={JSON.stringify([q, sort])}
      action="/courses"
      role="search"
      // Stops the browser restoring stale field values on back/forward without JS.
      autoComplete="off"
      className="mt-xl flex flex-col gap-md sm:flex-row sm:items-end"
    >
      <div className="min-w-0 sm:flex-1">
        <label htmlFor="catalog-q" className="type-label-md block">
          Search courses
        </label>
        <input
          id="catalog-q"
          type="search"
          name="q"
          defaultValue={q}
          placeholder="Title or topic"
          className={`${fieldClassName} mt-xs`}
        />
      </div>

      <div className="sm:w-[220px]">
        <label htmlFor="catalog-sort" className="type-label-md block">
          Sort by
        </label>
        <AutoSubmitSelect
          id="catalog-sort"
          name="sort"
          defaultValue={sort}
          className={`${fieldClassName} mt-xs`}
        >
          {Object.entries(SORT_LABELS).map(([value, label]) => (
            <option key={value} value={value}>
              {label}
            </option>
          ))}
        </AutoSubmitSelect>
      </div>

      <button type="submit" className="button-secondary">
        Search
      </button>
    </Form>
  );
}
