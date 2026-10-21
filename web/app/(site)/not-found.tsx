import { NotFoundMessage } from "@/components/not-found-message";

// Covers notFound() thrown inside the group; unmatched URLs render app/not-found.tsx.
export default function SiteNotFound() {
  return <NotFoundMessage />;
}
