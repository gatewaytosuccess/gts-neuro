import { Masthead } from "@/components/masthead";
import { NotFoundMessage } from "@/components/not-found-message";
import { SiteFooter } from "@/components/site-footer";

// Unmatched URLs render outside every route group, so this brings its own chrome.
export default function NotFound() {
  return (
    <>
      <Masthead />
      <NotFoundMessage />
      <SiteFooter />
    </>
  );
}
