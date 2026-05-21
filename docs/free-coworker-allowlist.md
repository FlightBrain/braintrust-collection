# Free coworker allowlist

The drop is configured as a **free, allowlisted mint** for coworkers. Each
approved wallet can claim exactly **one** NFT for **zero ETH** (plus a small
gas fee paid by the minter).

## Collecting addresses safely

1. Ask each coworker for their **public wallet address only**. It starts with `0x` and is 42 characters long.
2. Never ask for or accept a seed phrase, private key, or recovery phrase. If a coworker offers it, refuse and tell them to keep it private forever.
3. Store the list locally (not in a shared Google Doc). The example schema is in `data/allowlist.example.csv`.

## CSV format

```
name,slug,wallet_address,max_claimable,price,notes_optional
Alex Doe,alec,0x1234...abcd,3,0,
Sam Lee,sacha,0xabcd...1234,3,0,
```

- `name`: optional display name.
- `slug`: REQUIRED. The SDR this wallet is allowed to mint. Must be one of: alec, ava, catherine, chris, duncan, evan, garrett, joe, kensington, keslar, nick, owen, ryan, sacha, shaune.
- `wallet_address`: REQUIRED. 0x + 40 hex chars.
- `max_claimable`: 1 to 3. The coworker drop uses 3.
- `price`: must be `0` for the coworker drop.
- `notes_optional`: anything you want.

**Wallet-bound rule:** each wallet is mapped to exactly one SDR. That wallet can ONLY mint their own SDR's variants. Token IDs are deterministic: `slugIndex * 3 + walletClaimedCount`. For example, KB at slug "kensington" (index 8) mints tokens 24, 25, 26.

## Validate the list

```bash
npm run validate-allowlist -- data/allowlist.csv
```

Common errors: malformed addresses, duplicates, prices accidentally set above 0.

## Export to thirdweb CSV

```bash
npm run export-thirdweb-allowlist -- data/allowlist.csv data/allowlist.thirdweb.csv
```

Output schema: `address,maxClaimable,price,currencyAddress`. Verify thirdweb's current schema in the dashboard before upload (it has changed historically).

## Configure thirdweb claim phase

1. Open your contract in https://thirdweb.com/dashboard
2. **Claim Conditions** -> **Add Phase** (or edit the existing public phase).
3. Set:
   - `Name`: `Coworkers`
   - `Start`: `Now` (or a future timestamp)
   - `Supply`: `15`
   - `Price`: `0`
   - `Limit per wallet`: `1`
   - `Who can claim`: upload `data/allowlist.thirdweb.csv`
4. Disable any "Public" phase that overlaps.
5. Save + approve.

## Test

- Approved wallet: connect to the site, hit Mint, transaction should succeed.
- Unapproved wallet: connect to the site, hit Mint, transaction should revert with `DropClaimExceedLimit` or `not in allowlist`. The site surfaces this as "Wallet not on allowlist."

## What to tell coworkers

Use the template in `docs/coworker-wallet-request.md`. Do not send anything yet.
