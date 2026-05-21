# Backend infrastructure overview

A short tour of every piece, what it does, and what stays manual.

## Layers

```
artwork (public/nfts/, public/sdrs/, public/photos/, public/pixels/)
   |
   v
metadata generators (scripts/generate-metadata.ts, generate-collection-metadata.ts)
   |
   v
metadata files (public/metadata/{1..15}.json, collection.json)
   |
   v
IPFS pin (manual, one-time per CID)
   |
   v
on-chain contract (thirdweb DropERC721 on Base)
   |
   v
mint UI (app/page.tsx + components/MintCard.tsx)
   |
   v
wallet (RainbowKit + wagmi + Reown WalletConnect)
   |
   v
user
```

## What lives where

| Concern | File(s) |
|---|---|
| Chain config (Base + Sepolia + Ethereum) | `lib/chains.ts` |
| Env values | `lib/env.ts`, `.env.local`, `.env.base-sepolia.example`, `.env.base-mainnet.example` |
| Launch status | `lib/status.ts` |
| Wagmi + RainbowKit setup | `lib/wagmi.ts`, `app/providers.tsx` |
| Contract adapter | `lib/contract/adapter.ts`, `lib/contract/thirdwebDrop.ts`, `lib/contract/customErc721.ts`, `lib/contract.ts` |
| Mint UI | `components/MintCard.tsx`, `components/MintCardMock.tsx` |
| Mint preview (dev) | `app/dev/mint-states/page.tsx` |
| Status dashboard | `app/admin/status/page.tsx` |
| Read-only API | `app/api/status/route.ts`, `app/api/config/route.ts`, `app/api/metadata-summary/route.ts` |
| Allowlist tooling | `data/allowlist.example.csv`, `scripts/validate-allowlist.ts`, `scripts/export-thirdweb-allowlist.ts` |
| Metadata packaging | `scripts/package-metadata.ts`, `scripts/validate-production-metadata.ts` |
| Route smoke tests | `scripts/check-routes.ts` |
| Link scanner | `scripts/check-links.ts` |
| Env scanner | `scripts/check-env.ts` |
| Adapter smoke | `scripts/check-contract-adapter.ts` |

## What is automated

- Token metadata generation from `public/auto_people.json` + `public/rarity.json`.
- Collection metadata generation (`collection.json`, OpenSea-format).
- Metadata validation (`validate-metadata`, `validate-production-metadata`).
- Allowlist validation + thirdweb-CSV export.
- Metadata packaging (with sha256 checksums + upload README).
- Static smoke tests for routes + links.
- Env health check.
- Contract adapter sanity check.
- GitHub Actions CI (lint + build + safe validators).

## What stays manual

These all require wallet signing or external service interaction:

1. Wallet creation (MetaMask install + seed phrase backup).
2. Getting Sepolia ETH from a faucet.
3. Deploying the thirdweb contract.
4. Lazy-minting metadata items.
5. Setting claim phase.
6. Pinning to IPFS (any provider).
7. Setting `baseURI` and `contractURI` on the contract.
8. Verifying the contract on Basescan.
9. Pasting env vars into Vercel.
10. Listing on a marketplace (OpenSea, etc.).

Each of these has a doc under `docs/`.

## Endpoints you can hit anytime

- `GET /api/status` -> launch status + chain + contract configured (no secrets)
- `GET /api/config` -> public config (no secrets)
- `GET /api/metadata-summary` -> token count + IPFS readiness

## The site is safe to deploy without a contract

The MintCard renders a "contract not yet deployed" state when `NEXT_PUBLIC_CONTRACT_ADDRESS` is blank. No crash, no mint attempt, no contract reads. The rest of the site (gallery, FAQ, terms, privacy, license, legacy, picker, reveal, dev preview, admin status) works regardless.

## The site fails closed, not open

If any read fails, the UI shows a neutral state, not a fake "minted" state. Mint button is only enabled when wallet, chain, contract, and claim phase are all valid.
