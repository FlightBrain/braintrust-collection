# IPFS upload instructions

This folder contains everything you need to pin to IPFS or Arweave.

## Folder layout

- `tokens/{1..15}.json`: per-token metadata
- `collection.json`: collection-level metadata (OpenSea-style)
- `_manifest.json`: generation timestamp, mode, checksums, warnings

## Upload order (do not swap)

1. **Pin the art folder first** (public/nfts/corporate). Copy the CID.
2. Re-run with the new art URI:
   ```
   NEXT_PUBLIC_BASE_IMAGE_URI=ipfs://<art-cid>/ METADATA_MODE=ipfs npm run generate-metadata && npm run collection-metadata && npm run package-metadata
   ```
3. Pin THIS folder's `tokens/` (or the whole folder). Copy the CID.
4. Set the contract `baseURI` to `ipfs://<metadata-cid>/tokens/`.
5. Set the contract `contractURI` to `ipfs://<metadata-cid>/collection.json`.
6. Test `tokenURI(0)` on the contract.
7. Refresh metadata on the marketplace.

## Mode used for this build

- `METADATA_MODE=local`
- `NEXT_PUBLIC_BASE_IMAGE_URI=(empty)`

