import { DemoSwitch } from "@/components/demo-switch";
import { personaUserIds } from "@/lib/demo";

export function DemoBanner({ dark = false }: { dark?: boolean }) {
  const repoUrl = process.env.NEXT_PUBLIC_GITHUB_REPO_URL;

  return (
    <aside
      aria-label="About this demo"
      className={
        dark
          ? "border-b border-dark-rule bg-dark-surface text-dark-on-surface"
          : "border-b border-rule bg-tertiary-pale text-accent-strong"
      }
    >
      <div className="mx-auto flex max-w-[1200px] flex-wrap items-center justify-between gap-sm px-md py-sm sm:px-margin">
        <p className="type-body-sm">
          A demo with sample data, reset every night.
          {repoUrl && (
            <>
              {" "}
              <a
                href={repoUrl}
                className={`underline ${dark ? "text-dark-tertiary" : "text-tertiary-strong"}`}
              >
                View the code on GitHub
              </a>
            </>
          )}
        </p>
        <DemoSwitch userIds={personaUserIds()} dark={dark} />
      </div>
    </aside>
  );
}
