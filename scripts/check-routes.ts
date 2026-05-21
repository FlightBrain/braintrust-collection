/**
 * Smoke-tests every route on the deployed site. By default hits production.
 *
 * Usage:
 *   npm run check-routes
 *   BASE_URL=https://braintrust-collection.vercel.app npm run check-routes
 *   BASE_URL=http://localhost:3000 npm run check-routes
 */
const BASE_URL = process.env.BASE_URL ?? "https://braintrust-collection.vercel.app";

const ROUTES = [
  "/",
  "/gallery",
  "/faq",
  "/terms",
  "/privacy",
  "/license",
  "/admin/status",
  "/dev/mint-states",
  "/legacy.html",
  "/picker.html",
  "/reveal.html",
  "/variants/manifest.json",
  "/sdrs/assignments.json",
  "/metadata/1.json",
  "/metadata/collection.json",
];

async function check(url: string) {
  try {
    const res = await fetch(url, { redirect: "follow" });
    return { url, status: res.status, ok: res.ok };
  } catch (e) {
    return { url, status: 0, ok: false, error: (e as Error).message };
  }
}

async function main() {
  console.log(`=== Route check against ${BASE_URL} ===\n`);
  let failed = 0;
  for (const r of ROUTES) {
    const u = `${BASE_URL}${r}`;
    const result = await check(u);
    const sym = result.ok ? "PASS" : "FAIL";
    console.log(`  ${sym}  ${result.status}  ${r}`);
    if (!result.ok) failed++;
  }
  console.log(`\n${ROUTES.length - failed} / ${ROUTES.length} routes OK.`);
  process.exit(failed === 0 ? 0 : 1);
}

main();
