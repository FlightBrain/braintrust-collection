import { Header } from "@/components/Header";
import { FooterNav } from "@/components/FooterNav";

export default function LicensePage() {
  return (
    <main>
      <Header />
      <section className="mx-auto max-w-3xl px-6 pt-16 pb-20">
        <p className="font-mono text-[10px] uppercase tracking-[0.24em] text-muted">
          Legal
        </p>
        <h1 className="mt-2 text-4xl font-black tracking-tight md:text-5xl">
          License
        </h1>

        <div className="prose prose-invert mt-10 max-w-none text-sm leading-relaxed text-muted">
          <p className="text-white">
            Plain English: you own the NFT. You do not own the copyright in
            the artwork unless we explicitly say so below. You can display
            your NFT in your wallet, on your social profile, and in
            non-commercial settings without further permission.
          </p>

          <h2 className="mt-8 text-base font-bold text-white">
            1. What you receive
          </h2>
          <p>
            When you mint a token from the Collection, you receive ownership of
            that token as recorded on the blockchain. The token is a pointer
            to a metadata JSON file, which in turn points to an artwork file.
          </p>

          <h2 className="mt-8 text-base font-bold text-white">
            2. Personal-use license
          </h2>
          <p>
            For as long as you hold the token, you receive a personal,
            non-exclusive, worldwide, non-transferable license to:
          </p>
          <ul className="list-disc pl-6">
            <li>Display the artwork in your wallet, profile pictures, and on personal websites.</li>
            <li>Display the artwork in any context where you do not derive commercial revenue from it.</li>
            <li>Show the artwork to others to demonstrate ownership of the token.</li>
          </ul>

          <h2 className="mt-8 text-base font-bold text-white">
            3. What you do NOT receive
          </h2>
          <p>
            Unless explicitly stated in writing by the project owner, ownership
            of a token does NOT include:
          </p>
          <ul className="list-disc pl-6">
            <li>Copyright in the underlying artwork.</li>
            <li>Trademark rights in the Braintrust name or marks.</li>
            <li>The right to print, sell, license, sublicense, or otherwise
              commercialize the artwork.</li>
            <li>Permission to use the artwork to imply endorsement by Braintrust
              or by any individual depicted.</li>
          </ul>

          <h2 className="mt-8 text-base font-bold text-white">
            4. Transfer
          </h2>
          <p>
            When you transfer the token, the personal-use license transfers
            with it to the new holder. You lose the license the moment you no
            longer hold the token.
          </p>

          <h2 className="mt-8 text-base font-bold text-white">
            5. Likeness
          </h2>
          <p>
            The artwork depicts pixel-art likenesses of real people who have
            consented to being included in the Collection. Do not use the
            artwork in a way that defames, harasses, or misrepresents them.
          </p>

          <h2 className="mt-8 text-base font-bold text-white">
            6. Termination
          </h2>
          <p>
            The project owner may revoke the personal-use license, with notice,
            if the token holder uses the artwork in a manner that violates
            this License, the Terms, or applicable law.
          </p>

          <h2 className="mt-8 text-base font-bold text-white">
            7. Changes
          </h2>
          <p>
            We may update this License. Changes apply only to mints that occur
            after the update; rights for tokens already minted are not
            reduced retroactively.
          </p>
        </div>
      </section>
      <FooterNav />
    </main>
  );
}
