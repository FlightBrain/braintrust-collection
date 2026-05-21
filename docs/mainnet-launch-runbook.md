# Mainnet launch runbook

Use this only after every blocker in `legal-brand-consent-checklist.md` is cleared and `qa-checklist.md` testnet items have all passed.

## T-7 days

- [ ] Final legal sign-off
- [ ] Final brand sign-off
- [ ] Confirm royalty + treasury wallets (Gnosis Safe recommended)
- [ ] Confirm mint price + max-per-wallet
- [ ] Confirm sale start time
- [ ] Confirm metadata is pinned to IPFS (art + metadata, both CIDs saved)

## T-3 days

- [ ] Deploy a fresh thirdweb DropERC721 on **Base mainnet** (do not reuse the Sepolia contract). New address.
- [ ] Set ERC-2981 royalty recipient + percentage.
- [ ] Lazy-mint the 15 metadata items with the IPFS metadata CID.
- [ ] Configure claim phase: free, 1 per wallet, allowlist or open depending on plan.
- [ ] Verify the contract on Basescan ("Verify and Publish").

## T-1 day

- [ ] Update Vercel env vars to mainnet values (chain ID 8453, mainnet contract address, mainnet RPC, IPFS image URI).
- [ ] Trigger production redeploy.
- [ ] Visit https://braintrust-collection.vercel.app and confirm header pill reads "Mainnet" or "Live".
- [ ] Open `/admin/status` and confirm every category shows PASS (legal especially).
- [ ] Smoke-test one mint with a small wallet, confirm gas + ownership.

## Launch day

- [ ] Open Twitter/X announcement window
- [ ] Open Slack #pg-announcement window
- [ ] Confirm OpenSea collection page is live
- [ ] Confirm contract is verified
- [ ] Final smoke test
- [ ] Announce
- [ ] Monitor #c-* channels for issues for 60 minutes

## Anti-patterns

Do not:

- Deploy to mainnet with `NEXT_PUBLIC_BASE_IMAGE_URI` pointing at a Vercel URL. Pin to IPFS first.
- Skip the testnet pass.
- Skip the legal sign-off.
- Set royalty to 0 on mainnet (set 5% or whatever you choose, just not 0).
- Push to `main` without running `npm run prelaunch:strict` first.
- Use the deployer EOA as the long-term treasury. Move funds to a Safe.

## Rollback plan

If a critical bug ships:

1. Pause the sale via thirdweb dashboard (claim phase -> add a far-future start time, or disable).
2. Disable Vercel deployment promotion (deploy a "maintenance mode" page).
3. Investigate and patch before reopening.

There is no on-chain rollback for already-minted tokens. Communicate clearly with holders if anything goes wrong.
