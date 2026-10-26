import type { Metadata } from "next";
import { auth } from "@clerk/nextjs/server";
import Link from "next/link";
import { redirect } from "next/navigation";

import { Chevron } from "@/components/chevron";
import {
  fetchOrders,
  isAccountSuspended,
  type PurchasedOrder,
} from "@/lib/api";
import { formatDate, formatPrice } from "@/lib/format";

import { AccountTabs } from "../_components/account-tabs";
import { OrderStatusBadge } from "./_components/order-status-badge";

export const metadata: Metadata = {
  title: "Order history",
};

/** `null` when the API can't answer. */
async function loadOrders(): Promise<PurchasedOrder[] | null> {
  try {
    return await fetchOrders();
  } catch (error) {
    if (isAccountSuspended(error)) redirect("/suspended");
    return null;
  }
}

export default async function OrderHistoryPage() {
  const { userId, redirectToSignIn } = await auth();
  if (!userId) return redirectToSignIn();

  const orders = await loadOrders();

  return (
    <main className="mx-auto w-full max-w-[1200px] flex-1 px-md py-2xl sm:px-margin">
      <p className="type-label-caps text-accent">Your account</p>
      <h1 className="type-headline-md measure mt-md">Order history</h1>
      <AccountTabs current="orders" />

      {orders === null ? (
        <p className="type-body-sm mt-xl rounded-sm bg-warning-subtle px-sm py-sm text-warning">
          The order API is not responding, so your orders are unavailable.
        </p>
      ) : orders.length === 0 ? (
        <EmptyState />
      ) : (
        <OrderList orders={orders} />
      )}
    </main>
  );
}

function OrderList({ orders }: { orders: PurchasedOrder[] }) {
  return (
    <ul className="mt-xl border-b border-rule">
      {orders.map((order) => {
        const date = formatDate(order.created_at);
        return (
          <li key={order.id} className="border-t border-rule">
            <Link
              href={`/account/orders/${encodeURIComponent(order.id)}`}
              className="group -mx-sm flex items-center gap-md rounded-md px-sm py-md hover:bg-paper-raised"
            >
              <div className="flex min-w-0 flex-1 flex-col gap-sm sm:flex-row sm:items-center sm:gap-lg">
                <div className="min-w-0 flex-1">
                  <span className="sr-only">Receipt for the order of </span>
                  <time
                    dateTime={order.created_at}
                    className="type-caption text-meta-text"
                  >
                    {date}
                  </time>
                  <ul className="mt-xs">
                    {order.items.map((item) => (
                      <li
                        key={item.course_slug}
                        className="type-label-lg break-words text-accent-strong group-hover:text-primary"
                      >
                        {item.course_title}
                      </li>
                    ))}
                  </ul>
                </div>
                <div className="flex items-center gap-md">
                  <OrderStatusBadge status={order.status} />
                  <span className="type-data-md tabular-nums">
                    {formatPrice(order.total_cents)}
                  </span>
                </div>
              </div>
              <Chevron
                direction="right"
                className="text-meta-text transition-transform duration-100 group-hover:translate-x-[3px] group-hover:text-tertiary-strong motion-reduce:transition-none"
              />
            </Link>
          </li>
        );
      })}
    </ul>
  );
}

function EmptyState() {
  return (
    <div className="measure mt-xl">
      <p className="type-body-lg text-accent-strong">
        You haven&rsquo;t bought a course yet.
      </p>
      <Link href="/courses" className="button-primary mt-lg inline-block">
        Browse courses
      </Link>
    </div>
  );
}
