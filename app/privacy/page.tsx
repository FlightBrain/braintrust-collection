import { Header } from "@/components/Header";
import { FooterNav } from "@/components/FooterNav";

export default function PrivacyPage() {
  return (
    <main>
      <Header />
      <section className="mx-auto max-w-3xl px-6 pt-16 pb-20">
        <p className="font-mono text-[10px] uppercase tracking-[0.24em] text-muted">
          Legal
        </p>
        <h1 className="mt-2 text-4xl font-black tracking-tight md:text-5xl">
          Privacy
        </h1>

        <div className="prose prose-invert mt-10 max-w-none text-sm leading-relaxed text-muted">
          <p>
            This site does not collect personal information. We do not run
            third-party tracking, analytics, or advertising scripts on the mint
            flow.
          </p>

          <h2 className="mt-8 text-base font-bold text-white">
            Wallet addresses
          </h2>
          <p>
            When you connect a wallet or mint a token, your public wallet
            address becomes associated with the transaction on the blockchain.
            Blockchains are public ledgers: your address and transaction
            history are visible to anyone. We do not store or sell wallet data
            beyond what the chain itself records.
          </p>

          <h2 className="mt-8 text-base font-bold text-white">
            Logs and infrastructure
          </h2>
          <p>
            The site is hosted on Vercel. Vercel may collect standard server
            logs (request IP, user agent, status code) for operational
            purposes. See Vercel&apos;s privacy policy for details.
          </p>

          <h2 className="mt-8 text-base font-bold text-white">
            Wallet provider data
          </h2>
          <p>
            Your chosen wallet (MetaMask, Coinbase Wallet, etc.) is a separate
            product with its own privacy policy. We have no insight into the
            data your wallet shares with its operator.
          </p>

          <h2 className="mt-8 text-base font-bold text-white">
            Cookies
          </h2>
          <p>
            We use only the cookies/localStorage strictly necessary to remember
            your wallet connection. We do not set marketing or tracking
            cookies.
          </p>

          <h2 className="mt-8 text-base font-bold text-white">
            Questions
          </h2>
          <p>
            Reach out through the project&apos;s public channels listed in the
            README.
          </p>
        </div>
      </section>
      <FooterNav />
    </main>
  );
}
