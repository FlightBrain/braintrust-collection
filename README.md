# Braintrust Collection

NFT minting website for **Braintrust Collection: Genesis**. 15 hand-pixeled
collectible cards, designed as a 1/1 ERC-721 drop on Base.

Built with Next.js 14 App Router, wagmi v2, RainbowKit, Tailwind. The artwork
itself lives unchanged in `public/nfts/corporate/*.svg` and is referenced by
both the website and the on-chain metadata.

> **Status: not launch-ready.** The contract has not been deployed. Art has
> not been pinned to IPFS. A legally-blocking TODO around employee likeness
> consent is open. See **Launch readiness** below.

## Stack

- **Framework:** Next.js 14 (App Router) + TypeScript
- **Styling:** Tailwind CSS
- **Wallet:** RainbowKit + wagmi v2 + viem (supports MetaMask, Coinbase
  Wallet, WalletConnect, Rainbow, Trust, and more out of the box)
- **Chain:** Base mainnet (8453) by default, Base Sepolia (84532) for testnet.
  Configurable via env.
- **Art:** existing SVGs at `public/nfts/corporate/*.svg`. Do not modify.

## Local development

```bash
# 1. Install deps
npm install

# 2. Copy env template
cp .env.local.example .env.local
# Then fill in NEXT_PUBLIC_WALLETCONNECT_PROJECT_ID at minimum.

# 3. Run the dev server
npm run dev
# -> http://localhost:3000
```

## NPM scripts

| Command | Purpose |
|---|---|
| `npm run dev` | Local dev server |
| `npm run build` | Production build |
| `npm run start` | Run the built site |
| `npm run lint` | ESLint (Next.js core-web-vitals) |
| `npm run generate-metadata` | Emit ERC-721 metadata for each of the 15 tokens to `public/metadata/{id}.json` |
| `npm run collection-metadata` | Emit OpenSea-style collection metadata to `public/metadata/collection.json` |
| `npm run validate-metadata` | Validate every token + collection JSON, sequential IDs, IPFS readiness |
| `npm run prelaunch` | Runs lint, generate-metadata, collection-metadata, validate-metadata, and build |

## Environment variables

All vars are `NEXT_PUBLIC_*` (browser-exposed values only, no secrets).

| Variable | Purpose | Example |
|---|---|---|
| `NEXT_PUBLIC_CHAIN_ID` | Target chain ID | `8453` (Base) or `84532` (Base Sepolia) |
| `NEXT_PUBLIC_CHAIN_NAME` | Display name | `Base` |
| `NEXT_PUBLIC_RPC_URL` | RPC endpoint | `https://mainnet.base.org` |
| `NEXT_PUBLIC_CONTRACT_ADDRESS` | Deployed contract address | `0x...` |
| `NEXT_PUBLIC_TOTAL_SUPPLY` | Display fallback | `15` |
| `NEXT_PUBLIC_MINT_PRICE` | Display + tx value fallback (ETH) | `0.005` |
| `NEXT_PUBLIC_MARKETPLACE_URL` | OpenSea/etc. link | `https://opensea.io/collection/...` |
| `NEXT_PUBLIC_WALLETCONNECT_PROJECT_ID` | Required for WalletConnect. Public-safe. | `abc123...` from cloud.walletconnect.com |
| `NEXT_PUBLIC_BASE_IMAGE_URI` | Used by metadata generator | `ipfs://<cid>` once art is pinned |
| `NEXT_PUBLIC_FEE_RECIPIENT` | Royalty wallet (ERC-2981 + collection.json) | `0x...` |
| `NEXT_PUBLIC_SELLER_FEE_BPS` | Royalty in basis points | `500` (5%) |

When `NEXT_PUBLIC_CONTRACT_ADDRESS` is blank, the mint card renders a
"contract not yet deployed" state instead of crashing.

## Testnet walkthrough (Base Sepolia, REQUIRED before mainnet)

Mainnet launch is blocked until Base Sepolia mints pass end-to-end. Follow these steps in order. Do not skip.

The mint UI is wired to call **thirdweb DropERC721 `claim(receiver, quantity, currency, pricePerToken, AllowlistProof, data)`**, so you must deploy that contract type. See `lib/contract.ts` and `components/MintCard.tsx`.

### Step 1: Get Base Sepolia test ETH

You need ~0.05 Sepolia ETH for contract deployment + a few test mints.

Free faucets:
- https://www.alchemy.com/faucets/base-sepolia (recommended)
- https://faucet.quicknode.com/base/sepolia
- https://learnweb3.io/faucets/base_sepolia/

Connect the wallet you'll use as the deployer + treasury and claim a drip.

### Step 2: Deploy thirdweb NFT Drop on Base Sepolia

1. Go to https://thirdweb.com/dashboard
2. Connect the same wallet you funded in step 1.
3. Click **Contracts**, then **Deploy contract**.
4. Pick **Drops, then NFT Drop (ERC-721)**. Confirm it says "DropERC721".
5. Fill in:
   - **Name**: `Braintrust Collection (Sepolia Test)`
   - **Symbol**: `BTC-T` (or your pick)
   - **Image**: optional; can leave blank for the testnet contract
   - **Royalties**: recipient = your deployer wallet, percentage = `0` (testnet)
   - **Primary sale recipient**: your deployer wallet (treasury)
6. **Network**: select **Base Sepolia Testnet**. CRITICAL: do not pick Base mainnet.
7. Click **Deploy now**. Approve the deploy transaction in your wallet.
8. Once deployed, you'll land on the contract dashboard. **Copy the contract address** (top of page).

### Step 3: Upload the 15 metadata items (lazy mint)

In your local terminal, generate metadata with an HTTP base URL (Sepolia testing only):

```bash
# .env.local for testnet
NEXT_PUBLIC_BASE_IMAGE_URI=https://braintrust-collection.vercel.app

npm run generate-metadata
npm run collection-metadata
npm run validate-metadata
```

This writes `public/metadata/1.json` ... `public/metadata/15.json` referencing the live SVGs.

In the thirdweb dashboard:

1. Open your DropERC721 contract.
2. Click **NFTs** in the left nav.
3. Click **Batch upload**. Drag the 15 JSONs from `public/metadata/` (skip `_index.json` and `collection.json`).
4. thirdweb uploads them to IPFS, then asks you to confirm a "Lazy mint" transaction. Approve.
5. After it confirms, you should see 15 tokens listed, all currently unowned.

Note: this lazily prepares the tokens. They aren't minted to anyone yet, the `claim` function is what actually mints them on demand.

### Step 4: Configure the claim phase

1. In the contract dashboard, click **Claim Conditions**.
2. **Add Phase**:
   - **Name**: `Public`
   - **When will this phase start**: `Now`
   - **How many tokens will you drop in this phase**: `15`
   - **How much do you want to charge to claim**: `0`
   - **Limit per wallet**: `1`
   - **What currency**: leave default (native ETH)
   - **Who can claim**: **Any wallet** (no allowlist)
3. Save. Approve the transaction.

### Step 5: Set the Vercel env vars

Either in the Vercel dashboard (Project Settings, Environment Variables) or via the CLI:

```bash
# Required for the testnet site
NEXT_PUBLIC_CHAIN_ID=84532
NEXT_PUBLIC_CHAIN_NAME=Base Sepolia
NEXT_PUBLIC_CONTRACT_ADDRESS=0xYourSepoliaContractAddress
NEXT_PUBLIC_TOTAL_SUPPLY=15
NEXT_PUBLIC_MINT_PRICE=0
NEXT_PUBLIC_RPC_URL=https://sepolia.base.org
NEXT_PUBLIC_MARKETPLACE_URL=
```

Apply to **Production** and **Preview** environments.

### Step 6: Redeploy the site

The current Vercel CLI workflow:

```bash
cd ~/Desktop/braintrust-collection
rm -rf .next .vercel/output
npx vercel pull --yes --environment production
npx vercel build --prod --yes
npx vercel deploy --prebuilt --prod --yes
```

(or just `git push origin main` if Vercel auto-deploy from GitHub is on)

### Step 7: Smoke-test the mint flow

Open https://braintrust-collection.vercel.app in an incognito window. Verify each:

- [ ] Site loads with chain badge showing "Base Sepolia"
- [ ] Mint card shows price = Free, minted = 0 / 15, max per wallet = 1
- [ ] Click **Connect Wallet**, pick MetaMask, approve connection
- [ ] If you're on the wrong network, the **Switch to Base Sepolia** button appears. Click it.
- [ ] The mint button should now read **Mint free**. Click it. Approve the tx in your wallet.
- [ ] During pending, the card shows "Transaction pending".
- [ ] On success, card shows "Minted!" with a **View on Sepolia Basescan** link.
- [ ] Click the link. The tx confirms on https://sepolia.basescan.org.
- [ ] Refresh the page. Minted count shows 1 / 15.
- [ ] Try to mint a second time from the same wallet. The card should now show "You have reached the per-wallet claim limit" or similar reverted-tx state.
- [ ] Switch your wallet to Ethereum mainnet. The card shows "Wrong network" with a switch button.
- [ ] Switch back. The mint UI returns.
- [ ] Mint with a second wallet to confirm minted count goes to 2 / 15.

If all the boxes pass, the testnet flow is solid. Only THEN move to mainnet.

### Step 8: Inspect the contract on Sepolia Basescan

- [ ] Open `https://sepolia.basescan.org/address/<your contract>`
- [ ] **Read Contract** tab: call `nextTokenIdToMint()`. Should return the count of minted tokens.
- [ ] Call `getActiveClaimConditionId()`. Should return `0` (first phase).
- [ ] Call `getClaimConditionById(0)`. Should return your claim phase config (price=0, qty limit=1).
- [ ] Call `tokenURI(0)`. Should return `ipfs://<cid>/0` (thirdweb starts at 0).
- [ ] Call `contractURI()`. thirdweb auto-sets this.
- [ ] (Optional) Verify the contract on Basescan via the **Verify and Publish** tab so the reads are decoded nicely.

### Step 9: Check the metadata renders

- [ ] Open https://testnets.opensea.io/
- [ ] Search for your contract address. The collection should appear within a few minutes of the first mint.
- [ ] Each minted token should display the SVG art.
- [ ] If the thumbnail is missing, click into the token and hit **Refresh metadata**.

Once everything in steps 7-9 is green, you've cleared the testnet gate.

## Site structure

| Route | Purpose |
|---|---|
| `/` | Mint home: hero, mint card with all states, safety notice |
| `/gallery` | All 15 cards rendered from existing SVGs |
| `/faq` | FAQ (chain, how-to-mint, rights, storage, failures, royalties) |
| `/terms` | Terms of use |
| `/privacy` | Privacy policy |
| `/license` | NFT collector license with explicit copyright language |
| `/legacy.html` | Original interactive gallery (preserved verbatim) |
| `/picker.html` | Internal accessory picker (preserved) |
| `/reveal.html` | Internal reveal page (preserved) |

## Metadata generation

The art is already in `public/nfts/corporate/*.svg`. Generate metadata:

```bash
npm run generate-metadata     # writes public/metadata/{1..15}.json
npm run collection-metadata   # writes public/metadata/collection.json
npm run validate-metadata     # exits non-zero on any hard error
```

For production, set `NEXT_PUBLIC_BASE_IMAGE_URI` to your IPFS CID before
running the metadata scripts so the `image` field references decentralized
storage.

## IPFS upload order (do not deviate)

1. **Pin art first.** Upload `public/nfts/corporate/` (15 SVGs) to IPFS. Note
   the directory CID. Recommend CIDv1, base32 (starts with `b`), for best
   marketplace compatibility.
2. **Set image URI.** Update `.env.local`:
   ```
   NEXT_PUBLIC_BASE_IMAGE_URI=ipfs://<art-cid>
   ```
3. **Regenerate metadata** so it points at IPFS:
   ```bash
   npm run generate-metadata
   npm run collection-metadata
   ```
4. **Validate.**
   ```bash
   npm run validate-metadata
   ```
   The "image is an HTTP URL" warnings should be gone.
5. **Pin metadata.** Upload `public/metadata/` to IPFS. Note the metadata
   directory CID.
6. **Set the contract's `baseURI`** to `ipfs://<metadata-cid>/`. The contract
   will resolve `tokenURI(1)` to `ipfs://<metadata-cid>/1.json`.
7. **Set the contract's `contractURI`** (or thirdweb dashboard equivalent) to
   `ipfs://<metadata-cid>/collection.json` so marketplaces can pick up the
   collection-level fee + image.
8. **Keep local backups** of the SVGs and metadata in this repo so the
   collection can be re-pinned if a pinning service expires.

Recommended pinning providers: [Pinata](https://pinata.cloud) (free tier
sufficient for 15 files), [NFT.Storage](https://nft.storage),
[Filebase](https://filebase.com), [web3.storage](https://web3.storage).

## Contract deployment

You do not have a contract yet. Two recommended paths:

### Option A: thirdweb NFT Drop (no-code, fastest)

1. Go to [thirdweb.com/dashboard](https://thirdweb.com/dashboard)
2. Connect your wallet (the deployer wallet)
3. **Deploy contract**: Drops, then **NFT Drop (ERC-721)**
4. Chain: **Base Sepolia first**, then Base mainnet after testnet passes.
5. After deploy:
   - Set `Total supply` = 15
   - **Batch upload**: point at the IPFS metadata CID from above
   - Configure **Claim conditions**: price, max per wallet, start time
   - Set **Primary sale recipient** (treasury wallet)
   - Set **Royalty info**: recipient address + percentage (e.g. 5% = 500 bps)
   - Set **Collection metadata** to your `collection.json` CID
6. Copy the contract address into `.env` as `NEXT_PUBLIC_CONTRACT_ADDRESS`.
7. The mint button in this app calls `mint(quantity)` by default. thirdweb
   Drops use `claim(quantity)`. Edit `components/MintCard.tsx` and change
   `functionName: "mint"` to `functionName: "claim"`.

thirdweb NFT Drop supports out of the box: `totalSupply`, `maxSupply` (via
claim condition), `claim`, `tokenURI`, `contractURI`, ERC-2981 royalties.

### Option B: Custom OpenZeppelin ERC-721

1. Use [OpenZeppelin Contracts Wizard](https://wizard.openzeppelin.com/#erc721)
   to generate a minimal ERC-721 contract.
2. Required functions/features (the frontend reads these via the ABI shim in
   `lib/contract.ts`):
   - `mint(uint256 quantity)` payable
   - `totalSupply()` view returns (uint256)
   - `maxSupply()` view returns (uint256) (or hardcode 15)
   - `mintPrice()` view returns (uint256)
   - `paused()` view returns (bool)
   - `maxPerWallet()` view returns (uint256) (optional but recommended)
   - `contractURI()` view returns (string)  ← REQUIRED for marketplace fee/image
   - ERC-2981 `royaltyInfo(uint256, uint256)` ← REQUIRED for on-chain royalty
   - `withdraw()` only callable by owner ← treasury withdraw
3. Deploy via Hardhat or Foundry to Base Sepolia first.
4. Verify on Basescan/Sepolia.
5. Set `baseURI` to your IPFS metadata folder, `contractURI` to your
   collection.json.
6. Set ERC-2981 royalty recipient + bps to match `collection.json`.
7. Add the contract address to `.env`.

## Royalties (ERC-2981)

Set in two places, in this order:

1. **Off-chain marketplace hint** (`public/metadata/collection.json`):
   `seller_fee_basis_points` + `fee_recipient`. OpenSea/LooksRare/etc. read
   this when they index the collection.
2. **On-chain enforcement** (ERC-2981): the contract implements
   `royaltyInfo(tokenId, salePrice)` returning (recipient, amount).
   Marketplaces honor this where the contract supports ERC-2981.

**Royalties are NOT guaranteed everywhere.** Some marketplaces (Blur, X2Y2)
have moved to optional or zero royalties. Mention "creator earnings may apply
where supported by the marketplace and contract" in any sale copy. Do not
promise royalty income.

## Reveal strategy

This collection ships **instant reveal**: the moment a token is minted, its
metadata and image are public. No placeholder, no countdown reveal.

If you decide to switch to delayed reveal later:
- Contract must support a separate "placeholder" `baseURI` until reveal time.
- A separate `reveal()` function (owner-only) flips to the final `baseURI`.
- Add a "before reveal" placeholder image at `public/metadata/_placeholder.json`.
- Document the reveal trigger time on `/faq`.

`thirdweb NFT Drop` supports delayed reveal natively. OpenZeppelin custom
contracts need explicit code. Do not implement delayed reveal until you have
a contract that supports it.

## Sale configuration (fill these in before launch)

| Value | Current | Needed |
|---|---|---|
| Chain | Base mainnet (8453) | Confirm or change |
| Contract address | (none) | Deploy first |
| Total supply | 15 | Confirm (likely correct) |
| Mint price | (env var unset) | Decide (e.g. 0.005 ETH) |
| Max per wallet | (none) | Decide (e.g. 3, or unlimited) |
| Sale start time | (none) | Decide (unix timestamp or "open") |
| Allowlist / presale | None | Decide (probably none for 15 cards) |
| Treasury / withdraw wallet | (none) | Decide (Gnosis Safe recommended) |
| Royalty recipient | (none) | Decide (same as treasury, or split contract) |
| Royalty basis points | 500 (5%) default | Confirm |

## Marketplace readiness checklist

After contract is deployed and metadata is pinned:

- [ ] Verify the contract on Basescan (`Verify and Publish` tab). Required
      for OpenSea to display readable contract reads.
- [ ] Test `tokenURI(1)`, `tokenURI(7)`, `tokenURI(15)` directly via
      Basescan's "Read Contract" tab. Confirm they return the expected
      `ipfs://<cid>/N.json`.
- [ ] Test `contractURI()` returns the collection metadata URL.
- [ ] Open the collection on OpenSea (it auto-indexes within minutes of the
      first mint). Click each token, hit **Refresh metadata**.
- [ ] If thumbnails look wrong, IPFS hasn't propagated. Wait 5-15 min and
      refresh again.
- [ ] Add a collection banner + avatar via the OpenSea dashboard (1400x350
      banner, 350x350 avatar). The artwork can be a separate composition; do
      not modify the existing SVGs.
- [ ] Set `NEXT_PUBLIC_MARKETPLACE_URL` to the OpenSea collection URL and
      redeploy the site.
- [ ] Smoke test wallet mint from the production site.

## Production deploy

This repo is wired to Vercel.

```bash
# Test build locally
npm run prelaunch

# Push to GitHub. Vercel auto-deploys on push to main:
git add -A
git commit -m "deploy"
git push origin main
```

In the Vercel dashboard, paste all `NEXT_PUBLIC_*` env vars into Project
Settings > Environment Variables (under both Production and Preview
environments).

## Security

This site follows minting-site security basics:

- We **never** ask for seed phrases or private keys. Anywhere. Ever.
- Private keys never appear in this codebase.
- All env vars are `NEXT_PUBLIC_*` browser values only. **No secrets**.
- `WalletConnect` project ID is public-safe (it identifies the dApp, not the
  user).
- `.env.local` is gitignored.
- `.env.local.example` contains only placeholder values.
- The mint button disables during pending transactions.
- User-rejected transactions are handled gracefully.
- Insufficient-funds errors show a clear message.
- Wrong-network state surfaces a one-click switch button.
- Sold-out and paused states block mint without crashing.
- All external links use `target="_blank" rel="noreferrer noopener"`.
- No `dangerouslySetInnerHTML` in the React tree.
- No `eval`, no untrusted user input rendered unsafely.
- `npm audit` flags 17 moderate + 1 critical advisories on transitive deps
  inside the wagmi/MetaMask SDK chain. These are tracked upstream and don't
  affect the mint flow. Run `npm audit` periodically and bump when patches
  ship; don't `--force` upgrade these without testing.

## Legal / trust copy

The site states explicitly:

- NFTs in this collection are digital collectibles and art, not investments.
- No profit, resale, or floor price is promised.
- Nothing on the site is financial advice.
- Buying the NFT does not transfer copyright. See `/license`.
- Commercial rights only exist where explicitly granted (currently none).
- Creator earnings/royalties may apply where supported by the marketplace and
  contract, but are not guaranteed everywhere.
- We never request seed phrases or private keys.

These statements appear on `/`, `/faq`, `/terms`, and `/license`.

## Pre-launch BLOCKERS

These must be resolved before any mainnet announcement:

1. **Employee likeness consent.** The collection depicts 15 real Braintrust
   employees. Get **written consent from every depicted person** (and any
   relevant company approval) before the contract goes live on mainnet.
   Recommend a one-page release covering: name, likeness, derivative art,
   public collection. **THIS IS A LEGAL BLOCKER.**
2. **Braintrust brand approval.** The collection uses the Braintrust name,
   logo style, and "sales floor" reference. Get sign-off from whoever owns
   the Braintrust trademark and brand before launch.
3. Deploy contract on Base Sepolia, run the testnet checklist, mint at least
   one token through the production-style flow.
4. Pin art + metadata to IPFS, regenerate metadata, re-validate, re-pin.
5. Set every entry in the **Sale configuration** table.
6. Set ERC-2981 royalty info on the contract + match `collection.json`.
7. Verify the contract on Basescan.
8. Smoke test all mint states from the deployed Vercel site, on testnet.

## Launch readiness summary

| Category | Status |
|---|---|
| Local dev (`npm install`, `npm run dev`) | OK |
| Lint | OK (0 errors, 0 warnings) |
| Build | OK (9 routes prerendered) |
| Token metadata generation | OK (15 files) |
| Collection metadata generation | OK (placeholder `fee_recipient`) |
| Metadata validation | OK (0 errors, 15 warnings for HTTP image URLs, fix on IPFS pin) |
| Wallet (RainbowKit) | Configured |
| Chain config | Base mainnet by default, Base Sepolia ready via env |
| Mint states | All 11 states implemented (idle / connecting / wrong network / paused / live / pending / success / rejected / insufficient funds / sold out / contract not deployed) |
| Contract integration | PLACEHOLDER. No address. Site shows "contract not yet deployed" until env is set. |
| ERC-2981 royalties | Documented. Not enforced yet (no contract). |
| `contractURI` | Documented as required. Not yet on-chain. |
| IPFS pinning | Documented. Not done. |
| Legal pages | `/terms`, `/privacy`, `/license` shipped. Project-specific edits recommended (entity name, contact email). |
| Employee likeness consent | **BLOCKER. Not yet obtained.** |
| Braintrust brand approval | **BLOCKER. Not yet obtained.** |
| Testnet mint | NOT YET. Required before mainnet. |
| Mainnet mint | BLOCKED. |

## What was preserved unchanged

- `public/nfts/corporate/*.svg` (162 NFT card SVGs)
- `public/sdrs/*.png` (15 v20 portrait PNGs)
- `public/photos/*` (167 source photos)
- `public/pixels/*` (sprite assets)
- `public/legacy.html` (full original interactive gallery)
- `public/picker.html`, `public/reveal.html` (internal tools)

The Python pipeline (`character_builder.py`, `accessories_v3.py`,
`face_template_v2.py`, `assign.py`, `generate_v20_nfts.py`, etc.) is also
preserved unchanged in the repo root so the art can be regenerated if needed.
