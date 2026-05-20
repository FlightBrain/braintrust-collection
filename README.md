# Braintrust Collection

NFT minting website for **Braintrust Collection: Genesis**. 15 hand-pixeled
collectible cards, deployed as a 1/1 ERC-721 drop on Base.

Built with Next.js 14 App Router, wagmi v2, RainbowKit, Tailwind. The artwork
itself lives unchanged in `public/nfts/corporate/*.svg` and is referenced by
both the website and the on-chain metadata.

## Stack

- **Framework:** Next.js 14 (App Router) + TypeScript
- **Styling:** Tailwind CSS
- **Wallet:** RainbowKit + wagmi v2 + viem (supports MetaMask, Coinbase
  Wallet, WalletConnect, Rainbow, Trust, and more out of the box)
- **Chain:** Base (mainnet 8453, Sepolia 84532) by default. Configurable via
  env.
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

## Environment variables

All vars are `NEXT_PUBLIC_*` (browser-exposed).

| Variable | Purpose | Example |
|---|---|---|
| `NEXT_PUBLIC_CHAIN_ID` | Target chain ID | `8453` (Base) |
| `NEXT_PUBLIC_CHAIN_NAME` | Display name | `Base` |
| `NEXT_PUBLIC_RPC_URL` | RPC endpoint | `https://mainnet.base.org` |
| `NEXT_PUBLIC_CONTRACT_ADDRESS` | Deployed contract address | `0x...` |
| `NEXT_PUBLIC_TOTAL_SUPPLY` | Display fallback | `15` |
| `NEXT_PUBLIC_MINT_PRICE` | Display + tx value fallback (ETH) | `0.005` |
| `NEXT_PUBLIC_MARKETPLACE_URL` | OpenSea/etc. link | `https://opensea.io/collection/...` |
| `NEXT_PUBLIC_WALLETCONNECT_PROJECT_ID` | Required for WalletConnect | `abc123...` from cloud.walletconnect.com |
| `NEXT_PUBLIC_BASE_IMAGE_URI` | Used by metadata generator | `ipfs://<cid>` once art is pinned |

When `NEXT_PUBLIC_CONTRACT_ADDRESS` is blank, the mint card shows a "contract
not yet deployed" state instead of crashing.

## Site structure

| Route | Purpose |
|---|---|
| `/` | Mint home: hero, mint card with all states, safety notice |
| `/gallery` | All 15 cards rendered from existing SVGs |
| `/faq` | FAQ (chain, how-to-mint, rights, storage, failures) |
| `/terms` | Terms of use |
| `/privacy` | Privacy policy |
| `/license` | NFT collector license with explicit copyright language |
| `/legacy.html` | Original interactive gallery (preserved verbatim) |
| `/picker.html` | Internal accessory picker (preserved) |
| `/reveal.html` | Internal reveal page (preserved) |

## Generate metadata

The art is already in `public/nfts/corporate/*.svg`. To produce ERC-721
metadata JSON for each token:

```bash
npm run metadata
# -> writes public/metadata/{1..15}.json + public/metadata/_index.json
```

For production, set `NEXT_PUBLIC_BASE_IMAGE_URI` to your IPFS CID before
running this script so the `image` field references decentralized storage.

## Pin art + metadata to IPFS

Recommended providers: [NFT.Storage](https://nft.storage), [Pinata](https://pinata.cloud),
[Filebase](https://filebase.com), or [web3.storage](https://web3.storage).

```bash
# Example with Pinata CLI
npm install -g pinata-cli
pinata-cli auth <your-jwt>

# 1. Pin the 15 SVGs
pinata-cli pin public/nfts/corporate
# -> note the directory CID, e.g. bafybeig...

# 2. Update .env.local with the new BASE_IMAGE_URI:
#    NEXT_PUBLIC_BASE_IMAGE_URI=ipfs://bafybeig.../

# 3. Regenerate metadata so it points at IPFS
npm run metadata

# 4. Pin the metadata folder
pinata-cli pin public/metadata
# -> note the metadata directory CID

# 5. Set the contract baseURI to ipfs://<metadata-cid>/ (or via thirdweb UI)
```

## Deploy the contract

You do not have a contract yet. Two recommended paths:

### Option A: thirdweb NFT Drop (no-code, fastest)

1. Go to [thirdweb.com/dashboard](https://thirdweb.com/dashboard)
2. Connect your wallet (the deployer wallet)
3. **Deploy contract** -> Drops -> **NFT Drop (ERC-721)**
4. Chain: Base. Name: `Braintrust Collection`. Symbol: `BTC` (or your pick).
5. After deploy:
   - Set `Total supply` = 15
   - **Batch upload**: point at the IPFS metadata CID from above
   - Configure **Claim conditions**: price (e.g. 0.005 ETH), max per wallet,
     start time.
6. Copy the contract address into `.env` as `NEXT_PUBLIC_CONTRACT_ADDRESS`.
7. The mint button in this app calls `claim(quantity)`. thirdweb Drops use
   `claim`. Edit `components/MintCard.tsx` and change `functionName: "mint"`
   to `functionName: "claim"` if you go this route.

### Option B: Custom OpenZeppelin ERC-721

1. Use [OpenZeppelin Contracts Wizard](https://wizard.openzeppelin.com/#erc721)
   to generate a minimal ERC-721 contract.
2. Add a `mint(uint256 quantity)` function with `payable`, supply cap, max per
   wallet, and a `paused` flag.
3. Deploy via Hardhat or Foundry to Base.
4. Verify on Basescan.
5. Set `baseURI` to your IPFS metadata folder.
6. Add the contract address to `.env`.
7. The mint button in this app already calls `mint(quantity)` so no code
   change needed.

## Production deploy

This repo is already wired to Vercel. After updating `.env.local`:

```bash
# Test build locally
npm run build
npm run start

# Push to GitHub. Vercel auto-deploys on push to main:
git add -A
git commit -m "deploy v22 mint site"
git push origin main
```

In the Vercel dashboard, paste all `NEXT_PUBLIC_*` env vars into Project
Settings, Environment Variables.

## Launch checklist

- [ ] Deploy contract on Base (Option A or B above)
- [ ] Pin all 15 SVGs to IPFS, note the CID
- [ ] Run `npm run metadata` with `NEXT_PUBLIC_BASE_IMAGE_URI=ipfs://<cid>/`
- [ ] Pin `public/metadata/` to IPFS, note the metadata CID
- [ ] Set the contract `baseURI` to `ipfs://<metadata-cid>/`
- [ ] Test mint on Base Sepolia first (set `NEXT_PUBLIC_CHAIN_ID=84532`)
- [ ] Mint one yourself, verify it shows on Basescan
- [ ] Verify token metadata loads on OpenSea testnet
- [ ] Switch chain back to Base mainnet
- [ ] Get a WalletConnect Cloud project ID, set in env
- [ ] Set `NEXT_PUBLIC_MARKETPLACE_URL` once collection is listed on OpenSea
- [ ] Push final env vars to Vercel
- [ ] Smoke test all mint states: connect, wrong network, mint, success, error
- [ ] Review `/faq`, `/terms`, `/privacy`, `/license` for project-specific edits
- [ ] Confirm the `/legacy.html` route still loads
- [ ] Announce

## Security

This site follows minting-site security basics:

- We **never** ask for seed phrases or private keys. Anywhere. Ever.
- Private keys never appear in this codebase.
- All env vars are `NEXT_PUBLIC_*` browser values only. No secrets.
- The mint button disables during pending transactions.
- User-rejected transactions are handled gracefully.
- Insufficient-funds errors show a clear message.
- Wrong-network state surfaces a one-click switch button.
- Sold-out and paused states block mint without crashing.

## What is NOT here

- No referral system
- No reveal/blind-mint scheme
- No allowlist (yet; can be added once you have a list)
- No on-chain royalty enforcement (set this via marketplace settings)
- No "investment" copy. NFTs are art and collectibles, not financial
  instruments.

## What was preserved unchanged

- `public/nfts/corporate/*.svg`: 162 NFT card SVGs
- `public/sdrs/*.png`: 15 v20 portrait PNGs
- `public/photos/*`: 167 source photos
- `public/pixels/*`: sprite assets
- `public/legacy.html`: full original interactive gallery
- `public/picker.html`, `public/reveal.html`: internal tools

The Python pipeline (`character_builder.py`, `accessories_v3.py`,
`face_template_v2.py`, `assign.py`, `generate_v20_nfts.py`, etc.) is also
preserved unchanged in the repo root so the art can be regenerated if needed.
