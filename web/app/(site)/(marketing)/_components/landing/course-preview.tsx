import Link from "next/link";

import { CourseCard } from "@/components/course-card";
import { fetchCourses, type CourseSummary } from "@/lib/api";

import { SectionHeading } from "./section-heading";

const PREVIEW_COUNT = 3;

// Renders nothing when the API is down or no course is published.
export async function CoursePreview() {
  let courses: CourseSummary[];
  try {
    courses = (await fetchCourses()).results.slice(0, PREVIEW_COUNT);
  } catch {
    return null;
  }
  if (courses.length === 0) return null;

  return (
    <section
      aria-labelledby="courses-heading"
      className="mx-auto max-w-[1200px] px-md py-2xl sm:px-margin lg:py-3xl"
    >
      <SectionHeading
        id="courses-heading"
        eyebrow="The catalog"
        title="Recently published"
      />

      <ul className="mt-xl grid gap-gutter md:grid-cols-3">
        {courses.map((course) => (
          <li key={course.id}>
            <CourseCard course={course} heading="h3" />
          </li>
        ))}
      </ul>

      <div className="mt-xl">
        <Link href="/courses" className="button-secondary">
          Browse all courses
        </Link>
      </div>
    </section>
  );
}
