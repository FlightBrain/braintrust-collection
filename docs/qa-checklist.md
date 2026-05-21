# QA checklist

Run this before any deploy. Items grouped by what tooling you need.

## Local checks (no wallet, no contract)

- [ ] `npm install` succeeds
- [ ] `npm run lint` clean
- [ ] `npm run generate-metadata` produces 15 token JSONs
- [ ] `npm run collection-metadata` produces `collection.json`
- [ ] `npm run validate-metadata` returns 0 errors
- [ ] `npm run check-env` runs (warnings OK, no errors)
- [ ] `npm run check-contract` confirms thirdweb-drop is the active adapter
- [ ] `npm run check-links` clean
- [ ] `npm run build` prerenders all routes

## Visual checks (no wallet)

- [ ] `/dev/mint-states` renders all 17 mock states without crashing
- [ ] `/admin/status` shows accurate verdicts for every category
- [ ] Mobile menu opens on small viewport, closes on link click + Esc
- [ ] Hero buttons stack on mobile, side-by-side on desktop
- [ ] Mint card padding tight on mobile, comfortable on desktop
- [ ] Focus rings visible on every interactive control
- [ ] No layout shift when status pill loads

## Route checks (`npm run check-routes`)

- [ ] `/` 200
- [ ] `/gallery` 200
- [ ] `/faq` 200
- [ ] `/terms` 200
- [ ] `/privacy` 200
- [ ] `/license` 200
- [ ] `/dev/mint-states` 200
- [ ] `/admin/status` 200
- [ ] `/legacy.html` 200
- [ ] `/picker.html` 200
- [ ] `/reveal.html` 200
- [ ] `/api/status` 200, returns JSON
- [ ] `/api/config` 200, returns JSON
- [ ] `/api/metadata-summary` 200, returns JSON

## Wallet checks (when KB is back with phone)

- [ ] Connect MetaMask via WalletConnect QR
- [ ] Connect Coinbase Wallet
- [ ] Disconnect
- [ ] Switch to wrong network, button to switch back appears
- [ ] Switch successfully to Base Sepolia
- [ ] Mint button shows "Mint free"
- [ ] Click reject in wallet, error shows
- [ ] Approve mint, pending state appears
- [ ] Success state shows Sepolia Basescan link
- [ ] Second mint from same wallet shows per-wallet limit error

## Metadata checks (after IPFS pin)

- [ ] `METADATA_MODE=ipfs npm run validate-production-metadata` passes
- [ ] `npm run package-metadata` produces `dist/metadata-package/`
- [ ] `_manifest.json` checksums match
- [ ] Each token JSON's `image` field starts with `ipfs://`
- [ ] `collection.json` `image` field starts with `ipfs://`

## Marketplace checks (after first mint)

- [ ] Contract appears on OpenSea testnet
- [ ] Each minted token shows the SVG
- [ ] Collection banner / avatar set (optional)
- [ ] `NEXT_PUBLIC_MARKETPLACE_URL` set in Vercel

## Mainnet no-go (deploy blockers)

- [ ] **Employee likeness consent collected for every depicted person**
- [ ] **Braintrust brand approval obtained**
- [ ] Testnet mint flow passed
- [ ] Art pinned to IPFS with CID saved
- [ ] Metadata pinned to IPFS with CID saved
- [ ] Contract verified on Basescan
- [ ] ERC-2981 royalty info matches `collection.json`
- [ ] All "no investment" copy intact

If any item in this section is unchecked, do not proceed to mainnet.
