import { Header } from "@/components/Header";
import { FooterNav } from "@/components/FooterNav";
import { MintCardMock } from "@/components/MintCardMock";

export const metadata = {
  title: "Dev Preview · Mint States · Braintrust Collection",
  robots: { index: false, follow: false },
};

const STATES = [
  "disconnected",
  "connected",
  "wrong-network",
  "missing-contract",
  "allowlist-only",
  "not-allowlisted",
  "paused",
  "live-free",
  "live-paid",
  "sold-out",
  "pending-tx",
  "success",
  "rejected",
  "insufficient-funds",
  "sale-not-started",
  "metadata-pending",
  "marketplace-pending",
] as const;

export default function MintStatesDevPage() {
  return (
    <main>
      <Header />
      <section className="mx-auto max-w-6xl px-4 pb-12 pt-10 sm:px-6">
        <div className="mb-8 rounded-xl border border-legendary/40 bg-legendary/5 p-5 text-legendary">
          <p className="font-mono text-[10px] font-bold uppercase tracking-[0.24em]">
            Dev preview, not connected to any contract
          </p>
          <p className="mt-2 text-sm leading-relaxed text-white/80">
            Every state is rendered with mock data. No wallet, no contract
            read, no transaction. This page exists so we can visually QA all
            mint states without a deployed contract.
          </p>
        </div>

        <h1 className="text-3xl font-black tracking-tight md:text-4xl">
          Mint state preview
        </h1>
        <p className="mt-2 max-w-2xl text-sm leading-relaxed text-muted">
          {STATES.length} states. Each card is purely visual. Use this to
          confirm copy and styling before launch.
        </p>

        <div className="mt-10 grid grid-cols-1 gap-6 md:grid-cols-2 lg:grid-cols-3">
          {STATES.map((s) => (
            <div key={s}>
              <p className="mb-2 font-mono text-[10px] uppercase tracking-[0.2em] text-muted">
                {s}
              </p>
              <MintCardMock state={s} />
            </div>
          ))}
        </div>
      </section>
      <FooterNav />
    </main>
  );
}
