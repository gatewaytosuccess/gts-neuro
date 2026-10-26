import type { Metadata } from "next";
import Link from "next/link";
import { notFound } from "next/navigation";

import { Breadcrumbs } from "@/components/breadcrumbs";
import { ApiError, fetchAdminOrder, type AdminOrderDetail } from "@/lib/api";
import { formatPrice } from "@/lib/format";

import { formatDate, formatDateTime } from "../../_lib/format";
import { DemoDisabled } from "../../_components/demo-disabled";
import { requireAdmin } from "../../_lib/require-admin";
import { EnrollmentStatusBadge } from "../../users/_components/enrollments";
import { StatusBadge as AccountStatusBadge } from "../../users/_components/status-badge";
import { OrderStatusBadge } from "../_components/order-status-badge";

export const metadata: Metadata = {
  title: "Order · Admin",
};

export default async function AdminOrderPage({
  params,
}: PageProps<"/admin/orders/[id]">) {
  // Layouts don't re-render on client navigation, and a layout that skips
  // `children` still sends them in the RSC payload.
  if ((await requireAdmin()) !== "admin") return null;

  const { id } = await params;

  let order: AdminOrderDetail;
  try {
    order = await fetchAdminOrder(id);
  } catch (error) {
    if (error instanceof ApiError && error.status === 404) notFound();
    return (
      <div>
        <Crumbs />
        <p className="type-body-sm mt-md rounded-sm bg-warning-subtle px-sm py-sm text-warning">
          The course API is not responding, so this order is unavailable.
        </p>
      </div>
    );
  }

  const buyerName = order.buyer.name || order.buyer.email;

  return (
    <div>
      <Crumbs current={`Order of ${formatDate(order.created_at)}`} />
      <Header order={order} />

      <section aria-labelledby="buyer-heading" className="mt-2xl">
        <h2 id="buyer-heading" className="type-headline-sm">
          Buyer
        </h2>
        <Buyer buyer={order.buyer} />
      </section>

      <section aria-labelledby="items-heading" className="mt-3xl">
        <h2 id="items-heading" className="type-headline-sm">
          Courses
        </h2>
        <Summary order={order} />
      </section>

      {(order.status === "paid" ||
        order.refunded_cents > 0 ||
        order.refunded_at) && (
        <section aria-labelledby="refund-heading" className="mt-3xl">
          <h2 id="refund-heading" className="type-headline-sm">
            Refund
          </h2>
          <Refund order={order} buyerName={buyerName} />
        </section>
      )}

      <section aria-labelledby="payment-heading" className="mt-3xl">
        <h2 id="payment-heading" className="type-headline-sm">
          Payment
        </h2>
        <Payment order={order} />
      </section>

      <section aria-labelledby="enrollments-heading" className="mt-3xl">
        <h2 id="enrollments-heading" className="type-headline-sm">
          Enrollments
        </h2>
        <Enrollments order={order} buyerName={buyerName} />
      </section>
    </div>
  );
}

function Crumbs({ current }: { current?: string }) {
  return (
    <Breadcrumbs
      items={[
        { label: "Orders", href: "/admin/orders" },
        ...(current ? [{ label: current }] : []),
      ]}
    />
  );
}

function Header({ order }: { order: AdminOrderDetail }) {
  return (
    <header className="mt-md">
      <div className="flex flex-wrap items-center gap-md">
        <h1 className="type-headline-md measure">
          Order of{" "}
          <time dateTime={order.created_at}>
            {formatDate(order.created_at)}
          </time>
        </h1>
        <OrderStatusBadge status={order.status} />
      </div>
      <p className="type-data-md mt-xs break-all text-meta-text">{order.id}</p>
      <dl className="type-body-sm mt-sm flex flex-wrap gap-x-lg gap-y-xs text-meta-text">
        <div>
          <dt className="inline">Created </dt>
          <dd className="inline">
            <time dateTime={order.created_at}>
              {formatDateTime(order.created_at)}
            </time>
          </dd>
        </div>
        <div>
          <dt className="inline">Updated </dt>
          <dd className="inline">
            <time dateTime={order.updated_at}>
              {formatDateTime(order.updated_at)}
            </time>
          </dd>
        </div>
      </dl>
    </header>
  );
}

function Buyer({ buyer }: { buyer: AdminOrderDetail["buyer"] }) {
  return (
    <div className="mt-md">
      <div className="flex flex-wrap items-center gap-x-md gap-y-xs">
        <Link
          href={`/admin/users/${buyer.id}`}
          className="type-label-lg break-words text-accent-strong hover:text-primary hover:underline"
        >
          {buyer.name || buyer.email}
        </Link>
        <AccountStatusBadge status={buyer.status} />
      </div>
      {buyer.name && (
        <p className="type-body-sm mt-xs break-all text-meta-text">
          {buyer.email}
        </p>
      )}
    </div>
  );
}

function Summary({ order }: { order: AdminOrderDetail }) {
  return (
    <div className="measure mt-md">
      <ul>
        {order.items.map((item) => (
          <li
            key={item.course_id}
            className="flex items-baseline justify-between gap-md border-t border-rule py-sm"
          >
            <Link
              href={`/admin/courses/${item.course_id}`}
              className="type-label-lg min-w-0 break-words text-accent-strong hover:text-primary hover:underline"
            >
              {item.title}
            </Link>
            <span className="type-data-md tabular-nums">
              {formatPrice(item.unit_price_cents)}
            </span>
          </li>
        ))}
      </ul>

      <dl className="border-t border-border-strong pt-sm">
        <SummaryRow label="Subtotal">
          {formatPrice(order.subtotal_cents)}
        </SummaryRow>
        {order.coupon_code && (
          <SummaryRow label="Coupon">
            <span className="break-all">{order.coupon_code}</span>
          </SummaryRow>
        )}
        {order.discount_cents > 0 && (
          <SummaryRow label="Discount">
            &minus;{formatPrice(order.discount_cents)}
          </SummaryRow>
        )}
        <SummaryRow label="Total" emphasis>
          {formatPrice(order.total_cents)}
        </SummaryRow>
      </dl>
    </div>
  );
}

function SummaryRow({
  label,
  emphasis = false,
  children,
}: {
  label: string;
  emphasis?: boolean;
  children: React.ReactNode;
}) {
  return (
    <div className="flex items-baseline justify-between gap-md py-xs">
      <dt
        className={emphasis ? "type-label-lg" : "type-label-md text-meta-text"}
      >
        {label}
      </dt>
      <dd
        className={`min-w-0 text-right tabular-nums ${emphasis ? "type-label-lg" : "type-data-md"}`}
      >
        {children}
      </dd>
    </div>
  );
}

function Refund({
  order,
  buyerName,
}: {
  order: AdminOrderDetail;
  buyerName: string;
}) {
  const partial = order.refunded_cents < order.total_cents;
  const keptAccess =
    order.status === "refunded" &&
    order.enrollments.some((enrollment) => enrollment.status === "active");

  return (
    <>
      {order.refunded_cents > 0 ? (
        <RefundDetails order={order} partial={partial} />
      ) : (
        <p className="type-body-md mt-md">Nothing has been refunded.</p>
      )}
      {order.status === "paid" && <DemoDisabled className="mt-lg" />}
      {keptAccess && (
        <p className="type-body-sm mt-lg text-meta-text">
          {buyerName} still has access to this order&rsquo;s courses. Revoke it
          on{" "}
          <Link
            href={`/admin/users/${order.buyer.id}`}
            className="text-primary underline"
          >
            their page
          </Link>{" "}
          if needed.
        </p>
      )}
    </>
  );
}

function RefundDetails({
  order,
  partial,
}: {
  order: AdminOrderDetail;
  partial: boolean;
}) {
  return (
    <dl className="mt-md grid gap-x-md gap-y-xs sm:grid-cols-[max-content_1fr] sm:gap-y-md">
      <div className="contents">
        <dt className="type-label-caps text-meta-text">Amount</dt>
        <dd className="type-body-md">
          {formatPrice(order.refunded_cents)}
          {partial && ` of ${formatPrice(order.total_cents)}`}
        </dd>
      </div>
      {order.refunded_at && (
        <div className="contents">
          <dt className="type-label-caps text-meta-text">Refunded</dt>
          <dd className="type-body-md">
            <time dateTime={order.refunded_at}>
              {formatDateTime(order.refunded_at)}
            </time>
          </dd>
        </div>
      )}
      {order.refunded_by && (
        <div className="contents">
          <dt className="type-label-caps text-meta-text">By</dt>
          <dd className="type-body-md">
            <Link
              href={`/admin/users/${order.refunded_by.id}`}
              className="text-primary hover:underline"
            >
              {order.refunded_by.name || "An admin"}
            </Link>
          </dd>
        </div>
      )}
      {order.refund_reason && (
        <div className="contents">
          <dt className="type-label-caps text-meta-text">Reason</dt>
          <dd className="type-body-md measure whitespace-pre-line break-words">
            {order.refund_reason}
          </dd>
        </div>
      )}
    </dl>
  );
}

function Payment({ order }: { order: AdminOrderDetail }) {
  if (!order.receipt_url && !order.stripe_payment_url) {
    return (
      <p className="type-body-md mt-md text-meta-text">
        {order.status === "pending" || order.status === "expired"
          ? "No payment was taken for this order."
          : "Stripe has no receipt or payment on record for this order."}
      </p>
    );
  }

  return (
    <ul className="mt-md flex flex-wrap gap-md">
      {order.receipt_url && (
        <li>
          <ExternalLink href={order.receipt_url}>Stripe receipt</ExternalLink>
        </li>
      )}
      {order.stripe_payment_url && (
        <li>
          <ExternalLink href={order.stripe_payment_url}>
            Payment in the Stripe dashboard
          </ExternalLink>
        </li>
      )}
    </ul>
  );
}

function ExternalLink({
  href,
  children,
}: {
  href: string;
  children: React.ReactNode;
}) {
  return (
    <a
      href={href}
      target="_blank"
      rel="noopener noreferrer"
      className="button-secondary inline-flex"
    >
      {children}
      <span className="sr-only"> (opens in a new tab)</span>
    </a>
  );
}

function Enrollments({
  order,
  buyerName,
}: {
  order: AdminOrderDetail;
  buyerName: string;
}) {
  const headerClassName = "type-label-md px-sm py-sm text-accent";

  return (
    <>
      {order.enrollments.length === 0 ? (
        <p className="type-body-md mt-md">This order holds no enrollments.</p>
      ) : (
        <div className="mt-md overflow-x-auto">
          <table className="w-full min-w-[480px] border-collapse text-left">
            <thead>
              <tr className="border-b border-border-strong">
                <th scope="col" className={headerClassName}>
                  Course
                </th>
                <th scope="col" className={headerClassName}>
                  Status
                </th>
                <th scope="col" className={headerClassName}>
                  Revoked
                </th>
              </tr>
            </thead>
            <tbody>
              {order.enrollments.map((enrollment) => (
                <tr
                  key={enrollment.id}
                  className="border-b border-rule align-top"
                >
                  <td className="px-sm py-sm">
                    <Link
                      href={`/admin/courses/${enrollment.course_id}`}
                      className="type-label-lg break-words text-accent-strong hover:text-primary hover:underline"
                    >
                      {enrollment.title}
                    </Link>
                  </td>
                  <td className="px-sm py-sm">
                    <EnrollmentStatusBadge status={enrollment.status} />
                  </td>
                  <td className="type-data-md whitespace-nowrap px-sm py-sm text-meta-text">
                    {enrollment.revoked_at ? (
                      <time dateTime={enrollment.revoked_at}>
                        {formatDate(enrollment.revoked_at)}
                      </time>
                    ) : (
                      <span aria-label="Not revoked">—</span>
                    )}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
      <p className="type-body-sm mt-lg text-meta-text">
        Revoke or restore access on{" "}
        <Link
          href={`/admin/users/${order.buyer.id}`}
          className="text-primary underline"
        >
          {buyerName}&rsquo;s page
        </Link>
        .
      </p>
    </>
  );
}
