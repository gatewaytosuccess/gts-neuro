import { NextResponse, type NextRequest } from "next/server";

/** Checkout is off in the demo: `/checkout?course=<slug>` goes back to the course. */
export async function GET(request: NextRequest) {
  const slug = request.nextUrl.searchParams.get("course");
  const destination = slug
    ? `/courses/${encodeURIComponent(slug)}`
    : "/courses";
  return NextResponse.redirect(new URL(destination, request.url), 303);
}
