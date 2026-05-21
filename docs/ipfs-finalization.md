# IPFS finalization checklist

Order matters. Do not deviate.

## 1. Pin the art folder

```bash
# Pick one provider:
# - Pinata: https://pinata.cloud
# - NFT.Storage: https://nft.storage
# - web3.storage: https://web3.storage
# - thirdweb storage (auto if you use their dashboard upload)

# Example with Pinata CLI:
npm install -g pinata-cli
pinata-cli auth <your-jwt>
pinata-cli pin public/nfts/corporate
```

You'll get a directory CID like `bafybei...`. CIDv1 base32 (starts with `b`) is recommended.

**Save the art CID.**

## 2. Regenerate metadata with the IPFS image URI

```bash
NEXT_PUBLIC_BASE_IMAGE_URI=ipfs://<art-cid>/ \
METADATA_MODE=ipfs \
npm run generate-metadata && \
npm run collection-metadata && \
npm run validate-production-metadata
```

`validate-production-metadata` will fail if any image URL is still HTTP or pointing to localhost.

## 3. Package the metadata

```bash
METADATA_MODE=ipfs npm run package-metadata
```

Output goes to `dist/metadata-package/`:
- `tokens/{1..15}.json`
- `collection.json`
- `_manifest.json` (timestamps + sha256 checksums)
- `README-UPLOAD.md`

## 4. Pin the metadata folder

```bash
pinata-cli pin dist/metadata-package
```

**Save the metadata CID.**

## 5. Set the contract baseURI

In thirdweb dashboard, or via the contract directly:

- `baseURI` = `ipfs://<metadata-cid>/tokens/`
- `contractURI` = `ipfs://<metadata-cid>/collection.json`

## 6. Test tokenURI

On Basescan/Sepolia Basescan:

- Read contract -> `tokenURI(0)` -> should return `ipfs://<metadata-cid>/tokens/0` (thirdweb starts token IDs at 0).
- Open that URL in https://ipfs.io/ipfs/<metadata-cid>/tokens/0 to confirm the JSON loads and the image is accessible.

## 7. Refresh marketplace metadata

OpenSea auto-indexes within a few minutes of the first mint. If a thumbnail looks wrong, click into the token and hit **Refresh metadata**.

## Pinning provider options

| Provider | Free tier | Notes |
|---|---|---|
| Pinata | Yes (10 GB) | Most widely used. Stable. CIDv1 supported. |
| NFT.Storage | Yes | Maintained by Protocol Labs. NFT-focused. |
| web3.storage | Yes | Same parent org as NFT.Storage. |
| Filebase | Free + paid | S3-compatible API. Good for automation. |
| thirdweb storage | Built-in | Automatic when you upload via thirdweb dashboard. |
| Arweave | One-time pay | Permanent, not pinned. Different cost model. |

For 15 SVGs + 15 metadata JSONs, any free tier is more than enough.

## What to keep local

Keep `public/nfts/corporate/`, `public/metadata/`, and `dist/metadata-package/` in the repo as backups. If a pinning provider lapses, you can re-pin from local.

## What to never do

- Pin a `.env.local`, private key, or admin credentials. Anything you pin is **permanently public**.
- Use a single non-decentralized URL (like a Vercel preview link) for production metadata. Pinning services may expire; IPFS via CID is the safe target.
