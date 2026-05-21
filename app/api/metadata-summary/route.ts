import fs from "node:fs";
import path from "node:path";
import { NextResponse } from "next/server";

export const dynamic = "force-static";

export async function GET() {
  const dir = path.join(process.cwd(), "public", "metadata");
  if (!fs.existsSync(dir)) {
    return NextResponse.json({ token_count: 0, collection_metadata: false });
  }
  const files = fs.readdirSync(dir);
  const tokens = files.filter((f) => /^\d+\.json$/.test(f));
  const collection = files.includes("collection.json");
  // Detect IPFS vs HTTP without exposing the actual URI
  let imageScheme: "ipfs" | "arweave" | "http" | "unknown" = "unknown";
  if (tokens.length) {
    try {
      const sample = JSON.parse(fs.readFileSync(path.join(dir, tokens[0]), "utf-8"));
      const img = (sample.image ?? "") as string;
      if (img.startsWith("ipfs://")) imageScheme = "ipfs";
      else if (img.startsWith("ar://") || img.includes("arweave.net")) imageScheme = "arweave";
      else if (img.startsWith("http")) imageScheme = "http";
    } catch {}
  }
  return NextResponse.json({
    token_count: tokens.length,
    collection_metadata: collection,
    image_scheme: imageScheme,
    ipfs_ready: imageScheme === "ipfs",
  });
}
