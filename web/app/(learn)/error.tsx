"use client";

import Link from "next/link";

export default function LearnError({ retry }: { retry: () => void }) {
  return (
    <main className="mx-auto w-full max-w-[1200px] flex-1 px-md py-2xl sm:px-margin">
      <p className="type-label-caps text-dark-on-surface-meta">
        Something went wrong
      </p>
      <h1 className="type-headline-md measure mt-md">
        This lesson didn&rsquo;t load.
      </h1>
      <p className="type-body-lg measure mt-lg">
        Something went wrong on our side. Try again, and if it keeps happening,
        come back a little later.
      </p>

      <div className="mt-xl flex flex-wrap gap-md">
        <button
          type="button"
          onClick={() => retry()}
          className="button-primary-dark"
        >
          Try again
        </button>
        <Link href="/dashboard" className="button-secondary-dark">
          Go to your dashboard
        </Link>
      </div>
    </main>
  );
}
