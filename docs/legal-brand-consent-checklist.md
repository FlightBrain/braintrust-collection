# Legal, brand, and consent checklist

Mainnet launch is blocked until **every** item below is resolved. Do not announce, list on a marketplace, or open the public sale before this list is fully signed off.

## Employee likeness consent (BLOCKER)

The collection depicts 15 real Braintrust employees in pixel-art form.

- [ ] Written consent from **every depicted person** for:
  - Use of their likeness in pixel-art form
  - Distribution as an NFT (on-chain, public, permanent)
  - Resale / transfer of the token by future owners
  - Display on third-party marketplaces (OpenSea, etc.)
- [ ] Documented refusal handling: if anyone declines, remove or replace their card before launch.
- [ ] Storage of signed consent forms in a private location (not in this repo).
- [ ] Confirmation that depicted people are at least 18 / of legal age in their jurisdiction.

Recommend a one-page release covering all of the above.

## Braintrust brand approval (BLOCKER)

The collection uses the Braintrust name, "Braintrust Collection" branding, and the "sales floor" framing.

- [ ] Sign-off from whoever owns the Braintrust trademark / brand.
- [ ] Decision on whether the project is publicly affiliated with Braintrust or framed as personal art.
- [ ] If publicly affiliated, decision on royalty/treasury destination (personal vs company).
- [ ] If unaffiliated, all copy must avoid implying endorsement.

## Compliance copy (must remain on the site)

- [ ] FAQ states NFTs are art, not investment.
- [ ] License page explicitly says copyright is NOT transferred with the token.
- [ ] License clause on personal-use only unless explicitly granted otherwise.
- [ ] Terms states no profit, resale value, or floor price is promised.
- [ ] Privacy page accurate (no tracking + IP addresses logged by Vercel only).
- [ ] Royalty (ERC-2981) language: "may apply where supported by the marketplace, not guaranteed".
- [ ] Seed phrase / private key safety notice on home + FAQ.

## Marketing constraints

- [ ] No "investment", "moon", "alpha", "guaranteed", "floor", "passive income", "profit" anywhere in copy or social posts.
- [ ] No implication that holders gain financial returns.
- [ ] No promise of future utility (future drops, airdrops, access, etc.) unless explicitly committed.

## Treasury and wallet

- [ ] Primary sale recipient is a wallet KB controls (not a personal exchange-deposit address).
- [ ] Royalty recipient address documented in `collection.json` and on the contract via ERC-2981.
- [ ] (Recommended) Royalty + treasury go to a Gnosis Safe rather than a single EOA.

## Final go/no-go

- [ ] Testnet mint flow passed end-to-end (see `qa-checklist.md`).
- [ ] Pinning service confirmed (Pinata or equivalent).
- [ ] Contract verified on Basescan.
- [ ] OpenSea collection renders correctly on testnet.
- [ ] Every item above is checked off.

When every item is checked, mainnet launch is unblocked.
