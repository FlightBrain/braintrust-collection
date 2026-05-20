import { Header } from "@/components/Header";
import { FooterNav } from "@/components/FooterNav";

export default function TermsPage() {
  return (
    <main>
      <Header />
      <section className="mx-auto max-w-3xl px-6 pt-16 pb-20">
        <p className="font-mono text-[10px] uppercase tracking-[0.24em] text-muted">
          Legal
        </p>
        <h1 className="mt-2 text-4xl font-black tracking-tight md:text-5xl">
          Terms of Use
        </h1>

        <div className="prose prose-invert mt-10 max-w-none text-sm leading-relaxed text-muted">
          <p>
            These Terms govern your use of this website and the minting of
            Braintrust Collection: Genesis (the &ldquo;Collection&rdquo;).
            By connecting your wallet or minting a token you agree to these
            Terms.
          </p>

          <h2 className="mt-8 text-base font-bold text-white">1. Eligibility</h2>
          <p>
            You must be at least 18 years old and legally able to enter
            contracts in your jurisdiction. You are responsible for confirming
            that participating is lawful where you live.
          </p>

          <h2 className="mt-8 text-base font-bold text-white">
            2. Nature of the Collection
          </h2>
          <p>
            Each token is a digital collectible: an ERC-721 token referencing
            artwork. NFTs in this Collection are art and are not offered as
            investments, securities, or financial instruments. There is no
            promise or expectation of profit.
          </p>

          <h2 className="mt-8 text-base font-bold text-white">
            3. As-is, no warranty
          </h2>
          <p>
            The Collection, this website, and the underlying smart contracts are
            provided &ldquo;as is&rdquo;. No warranty of merchantability,
            fitness for a particular purpose, uptime, or future utility is
            offered.
          </p>

          <h2 className="mt-8 text-base font-bold text-white">
            4. Wallets and transactions
          </h2>
          <p>
            You are solely responsible for the security of your wallet, your
            private keys, and the transactions you sign. We never request your
            seed phrase or private keys. Transactions on the blockchain are
            irreversible.
          </p>

          <h2 className="mt-8 text-base font-bold text-white">
            5. Intellectual property
          </h2>
          <p>
            See the License page for the rights granted with each token.
            Ownership of a token does not transfer copyright in the artwork
            unless explicitly stated.
          </p>

          <h2 className="mt-8 text-base font-bold text-white">
            6. Prohibited use
          </h2>
          <p>
            Do not use the Collection or the tokens for unlawful, fraudulent,
            harassing, or hateful purposes. We reserve the right to disassociate
            from any token that is used to promote such content.
          </p>

          <h2 className="mt-8 text-base font-bold text-white">
            7. Changes
          </h2>
          <p>
            We may update these Terms. Continued use of the site after an update
            constitutes acceptance.
          </p>

          <h2 className="mt-8 text-base font-bold text-white">
            8. Contact
          </h2>
          <p>
            For questions, reach out through the project&apos;s public channels
            listed in the README.
          </p>
        </div>
      </section>
      <FooterNav />
    </main>
  );
}
