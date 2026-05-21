# Vercel environment variables walkthrough

## Open the project

1. https://vercel.com/dashboard
2. Click the `braintrust-collection` project.
3. Go to **Settings**.
4. Click **Environment Variables** in the left nav.

## Variables to add

All of these are `NEXT_PUBLIC_*` (browser-safe). None of them are secrets.

| Key | Value (Base Sepolia) | Value (Base Mainnet) |
|---|---|---|
| `NEXT_PUBLIC_CHAIN_ID` | `84532` | `8453` |
| `NEXT_PUBLIC_CHAIN_NAME` | `Base Sepolia` | `Base` |
| `NEXT_PUBLIC_RPC_URL` | `https://sepolia.base.org` | `https://mainnet.base.org` |
| `NEXT_PUBLIC_CONTRACT_ADDRESS` | your testnet contract | your mainnet contract |
| `NEXT_PUBLIC_TOTAL_SUPPLY` | `15` | `15` |
| `NEXT_PUBLIC_MINT_PRICE` | `0` | `0` (free coworker drop) |
| `NEXT_PUBLIC_WALLETCONNECT_PROJECT_ID` | `1244257340c4eca87602fb431b8ec3a9` | same |
| `NEXT_PUBLIC_MARKETPLACE_URL` | leave empty | OpenSea URL after listing |
| `NEXT_PUBLIC_BASE_IMAGE_URI` | `https://braintrust-collection.vercel.app` (testnet OK) | `ipfs://<cid>` (required) |
| `NEXT_PUBLIC_FEE_RECIPIENT` | your wallet | your wallet or treasury |
| `NEXT_PUBLIC_SELLER_FEE_BPS` | `0` | `500` (5%) or whatever you choose |
| `NEXT_PUBLIC_CONTRACT_MODE` | `thirdweb-drop` | `thirdweb-drop` |

## Where to apply each

For every variable above:

- check **Production**
- check **Preview**
- check **Development**

Then click **Save**.

## Verify

Run:

```bash
cd ~/Desktop/braintrust-collection
npx vercel env ls
```

You should see each variable listed with the right environments.

## Redeploy so the new values take effect

```bash
rm -rf .next .vercel/output
npx vercel pull --yes --environment production
npx vercel build --prod --yes
npx vercel deploy --prebuilt --prod --yes
```

## Confirm

Open https://braintrust-collection.vercel.app. The header status pill should reflect the new chain. If `NEXT_PUBLIC_CONTRACT_ADDRESS` is set, the mint card should show stats + a mint button. If not, it shows "contract not yet deployed".

You can also hit https://braintrust-collection.vercel.app/api/config and https://braintrust-collection.vercel.app/api/status to see what the deployed build sees.

## Safety reminders

- Every variable here is publicly visible to users. That is fine because none of them are secrets.
- NEVER add a private key, seed phrase, or admin key. Vercel env vars are the wrong place for those.
- The WalletConnect/Reown project ID is also public-safe.
