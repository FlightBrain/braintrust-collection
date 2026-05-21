# thirdweb on Base Sepolia: step-by-step

This walkthrough deploys a free, allowlisted NFT Drop contract on Base
Sepolia (testnet) using thirdweb's no-code dashboard. No mainnet. No real
money. Use this exact order.

## Before you start

You need:

1. A wallet (MetaMask, Rainbow, Coinbase Wallet, etc.) on your phone or as a browser extension.
2. About 0.05 Sepolia ETH for gas. It's free from a faucet.

You do NOT need:

- A seed phrase pasted anywhere on a website. Never share your seed phrase.
- Real ETH. This is testnet.
- A mainnet contract. Not yet.

## Step 1: Get Sepolia ETH

1. Visit https://www.alchemy.com/faucets/base-sepolia
2. Sign in with Google.
3. Paste your wallet's public address (starts with `0x`).
4. Click "Send me ETH".

You should see the balance show up in your wallet within a minute.

## Step 2: Connect to thirdweb

1. Open https://thirdweb.com/dashboard
2. Click "Connect Wallet" (top right).
3. Pick your wallet, approve the connection.

## Step 3: Deploy NFT Drop

1. Click **Contracts** in the left nav.
2. Click **Deploy contract**.
3. Pick **Drops** category, then **NFT Drop (ERC-721)**.
4. Confirm the contract name is `DropERC721`.

Fill in:

| Field | Value |
|---|---|
| Name | `Braintrust Collection (Sepolia Test)` |
| Symbol | `BTC-T` |
| Image | leave blank for testnet |
| Royalties: Recipient | your wallet address |
| Royalties: Percentage | `0` (testnet) |
| Primary sale recipient | your wallet address |
| Platform fees | accept defaults |

Network: **Base Sepolia Testnet**. Do NOT pick Base mainnet.

Click **Deploy now**. Approve the deploy transaction.

When it lands, you'll be on the contract dashboard. Top of page: **copy the contract address**. Looks like `0xAbC123...`.

## Step 4: Upload metadata (lazy mint)

On your laptop, in the repo:

```bash
npm run generate-metadata
npm run collection-metadata
npm run validate-metadata
```

This produces `public/metadata/1.json` through `15.json` plus `collection.json`. Image URLs point to the live Vercel SVGs for testnet (no IPFS needed).

In the thirdweb dashboard:

1. Click **NFTs** in the left nav.
2. Click **Batch upload**.
3. Drag in the 15 JSONs from `public/metadata/`. Skip `_index.json` and `collection.json`.
4. thirdweb uploads to IPFS, then asks you to confirm a "Lazy mint" transaction. Approve.

After it confirms, you'll see 15 tokens listed, all unowned. They aren't minted to anyone yet, `claim` is what mints them on demand.

## Step 5: Configure the claim phase

1. Click **Claim Conditions**.
2. Click **Add Phase**.

| Field | Value |
|---|---|
| Name | `Public` |
| When will this phase start | `Now` |
| How many tokens will you drop in this phase | `15` |
| How much do you want to charge to claim | `0` |
| Limit per wallet | `1` |
| What currency | leave default (native ETH) |
| Who can claim | `Any wallet` (for the open test) |

Click **Save phases**. Approve the tx.

For the **allowlist-only test** (free coworker mint test):

1. Set "Who can claim" to a CSV upload.
2. Upload `data/allowlist.example.csv` (or your real list).
3. Save.

## Step 6: Paste the contract address into Vercel

In the Vercel dashboard:

1. Open Project Settings.
2. Environment Variables.
3. Add (or update):

```
NEXT_PUBLIC_CHAIN_ID=84532
NEXT_PUBLIC_CHAIN_NAME=Base Sepolia
NEXT_PUBLIC_CONTRACT_ADDRESS=0xYourSepoliaContract
NEXT_PUBLIC_RPC_URL=https://sepolia.base.org
NEXT_PUBLIC_TOTAL_SUPPLY=15
NEXT_PUBLIC_MINT_PRICE=0
```

Apply to **Production** and **Preview**.

## Step 7: Redeploy

```bash
cd ~/Desktop/braintrust-collection
rm -rf .next .vercel/output
npx vercel pull --yes --environment production
npx vercel build --prod --yes
npx vercel deploy --prebuilt --prod --yes
```

## Step 8: Test the mint

Open https://braintrust-collection.vercel.app on your phone (or in an incognito window with your wallet extension).

- Click **Connect Wallet**.
- The mint card should read "Mint free".
- Click it, approve the transaction.
- Confirm the success state shows a Sepolia Basescan link.
- Refresh: minted goes from 0 / 15 to 1 / 15.

## Step 9: Confirm on Sepolia Basescan

- Open `https://sepolia.basescan.org/address/<your contract>`
- **Read Contract** tab: try `nextTokenIdToMint()` (should be 1), `getActiveClaimConditionId()` (should be 0), `tokenURI(0)`.
- **Verify and Publish** the contract (optional but recommended) so the reads display nicely.

## What you can share publicly

- Public wallet address (`0x...`)
- Contract address (`0x...`)

## What you should NEVER share

- Seed phrase / recovery phrase
- Private key
- Mnemonic words

Anyone asking for these is trying to steal your wallet.
