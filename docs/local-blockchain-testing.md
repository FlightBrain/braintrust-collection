# Local blockchain testing (Hardhat)

When Base Sepolia faucets are jammed, you can still test the entire mint flow
end-to-end on a local Hardhat node. Same UI, same wallet, same contract ABI,
no real ETH required.

## What this gives you

- A local Ethereum-compatible chain at `http://127.0.0.1:8545` (chain id `31337`)
- A LocalMockDrop contract that mimics thirdweb DropERC721 closely enough that
  the existing MintCard works unchanged
- 20 pre-funded Hardhat test accounts (with 10000 fake ETH each)
- Your real MetaMask wallet pre-funded with 10 fake ETH so you can connect
  without importing any private keys

## What this is NOT

- A substitute for Base Sepolia. Real testnet/mainnet still requires real Base
  Sepolia ETH and a thirdweb deploy. This is a faucet-free fallback.
- Production. The LocalMockDrop contract is not audited, has no allowlist
  enforcement, has no royalty enforcement, and exists only for frontend
  testing.
- Private. Local Hardhat keys are well-known and the same on every machine.
  Never send real funds to them.

## Setup (one time)

```bash
cd ~/Desktop/braintrust-collection
npm install
npm run contract:compile
```

`npm install` adds Hardhat + OpenZeppelin + ethers. `contract:compile` runs
`hardhat compile` which produces ABI/bytecode under `.cache/hardhat-artifacts/`.

## Run the local chain

```bash
# Terminal 1: keep this running while you test.
npm run chain:local
```

You'll see "Started HTTP and WebSocket JSON-RPC server at http://127.0.0.1:8545".
Hardhat prints 20 test accounts with their private keys; ignore them, you
will not need to import any.

## Deploy the contract

```bash
# Terminal 2: run once per chain start.
npm run contract:deploy:local
```

The script will:

1. Deploy LocalMockDrop with name `Braintrust Collection (Local)`, symbol `BTC-L`, max supply 15
2. Set `baseURI` to `https://braintrust-collection.vercel.app/metadata/` so the live token JSONs resolve
3. Send 10 ETH (fake, local-only) from Hardhat account 0 to your real MetaMask wallet `0x6D0a...208E`
4. Write `.env.localchain.generated` with the deployed address + chain config

## Point the site at the local chain

```bash
# Copy the generated env into .env.local
cp .env.localchain.generated .env.local

# Start the Next.js dev server
npm run dev
```

The dev site runs at http://localhost:3000.

## Connect MetaMask to the local chain

In MetaMask:

1. Click the network picker (top of the wallet UI).
2. "Add network" / "Add a network manually".
3. Fill in:
   - Network Name: `Localhost`
   - New RPC URL: `http://127.0.0.1:8545`
   - Chain ID: `31337`
   - Currency Symbol: `ETH`
   - Block explorer: leave blank
4. Save.
5. Switch MetaMask to `Localhost`.

You should see 10 ETH in your wallet (the deploy script pre-funded you).

## Mint

1. Open http://localhost:3000.
2. The header pill should read "Testnet live" (the chain id is 31337, contract is configured).
3. Click **Connect Wallet**, pick MetaMask, approve.
4. The mint card should read "Free coworker mint, 1 per wallet".
5. Click **Mint free**. MetaMask asks you to sign. Approve.
6. Success state shows. The token is in your wallet (MetaMask "NFTs" tab if your version of MetaMask supports it).

## Reset

Each time you restart `npm run chain:local`, the chain state is wiped. You
need to re-run `contract:deploy:local` to get a fresh contract address. Then
re-copy `.env.localchain.generated` to `.env.local` and restart `npm run dev`.

## When this is NOT enough

Use Base Sepolia (the real testnet) when you want:

- A persistent chain other people can hit
- An OpenSea testnet listing
- A thirdweb dashboard UI for the contract
- A test of the actual thirdweb DropERC721 contract (not our mock)
- Anything that needs `claim` to behave 1:1 with thirdweb's production logic

Once Sepolia faucets unblock, the testnet path in
`docs/thirdweb-base-sepolia-walkthrough.md` is still the right gate before
mainnet.

## Safety

- Hardhat private keys are deterministic and **publicly known**. Do not send
  real ETH to any Hardhat address.
- Never import a Hardhat private key into a wallet you use on mainnet.
- The LocalMockDrop contract has no security audits and skips allowlist
  enforcement on purpose. It is for local UI testing only.
