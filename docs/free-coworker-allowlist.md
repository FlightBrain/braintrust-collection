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
name_optional,email_optional,wallet_address,max_claimable,price,notes_optional
Alex Doe,,0x1234...abcd,1,0,
Sam Lee,,0xabcd...1234,1,0,
```

- `name_optional`, `email_optional`, `notes_optional`: leave blank if you prefer.
- `wallet_address`: required.
- `max_claimable`: should be `1` per wallet for the coworker drop.
- `price`: should be `0` for the coworker drop.

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
