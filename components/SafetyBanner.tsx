export function SafetyBanner() {
  return (
    <div className="mx-auto mt-8 max-w-3xl rounded-xl border border-line bg-panel/60 px-5 py-4 text-xs leading-relaxed text-muted">
      <p className="mb-1 font-mono text-[10px] font-semibold uppercase tracking-[0.2em] text-accent">
        Security notice
      </p>
      <p>
        We will <span className="font-semibold text-white">never</span> ask for your
        seed phrase or private keys. Only sign transactions that you initiate.
        Treat this site like any other website: verify the URL, double-check the
        transaction details in your wallet, and never approve unlimited spend
        without reading what you are signing.
      </p>
    </div>
  );
}
