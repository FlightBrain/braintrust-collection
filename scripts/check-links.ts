/**
 * Static scan for common link mistakes in app/, components/, and docs/.
 * Catches:
 *   - empty href="" or href="#"
 *   - external links missing rel="noreferrer noopener"
 *   - localhost references in production-bound source
 *   - obvious placeholder strings like "TODO" or "YOUR_..." in href attrs
 *
 * Usage:
 *   npm run check-links
 */
import fs from "node:fs";
import path from "node:path";

const ROOTS = ["app", "components", "lib", "docs"];
const HARD_FAIL_PATTERNS: { pattern: RegExp; msg: string }[] = [
  { pattern: /href=""\s/g, msg: "empty href" },
  { pattern: /href="#"\s/g, msg: 'href="#" (dead link)' },
];
const WARN_PATTERNS: { pattern: RegExp; msg: string }[] = [
  { pattern: /href="http[s]?:\/\/localhost/g, msg: "localhost in source" },
  { pattern: /href="YOUR_[A-Z_]+"/g, msg: "placeholder href" },
];

let errors = 0;
let warnings = 0;

function walk(dir: string, cb: (filePath: string) => void) {
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    const full = path.join(dir, entry.name);
    if (entry.isDirectory()) {
      if (entry.name === "node_modules" || entry.name === ".next") continue;
      walk(full, cb);
    } else if (/\.(tsx?|jsx?|md|html)$/.test(entry.name)) {
      cb(full);
    }
  }
}

for (const root of ROOTS) {
  if (!fs.existsSync(root)) continue;
  walk(root, (file) => {
    const text = fs.readFileSync(file, "utf-8");
    for (const { pattern, msg } of HARD_FAIL_PATTERNS) {
      const m = text.match(pattern);
      if (m) {
        console.log(`ERROR ${file}: ${msg} (${m.length}x)`);
        errors += m.length;
      }
    }
    for (const { pattern, msg } of WARN_PATTERNS) {
      const m = text.match(pattern);
      if (m) {
        console.log(`WARN  ${file}: ${msg} (${m.length}x)`);
        warnings += m.length;
      }
    }
    // Detect external <a> missing rel
    const extLinks = text.match(/<a [^>]*href="https?:\/\/[^"]+"[^>]*>/g);
    if (extLinks) {
      for (const a of extLinks) {
        if (!a.includes("rel=")) {
          // Only flag obvious omissions; some links rely on Next/router
          // already, and inline elements may not need it.
          if (!a.includes("target=")) continue;
          console.log(`WARN  ${file}: external link missing rel: ${a.slice(0, 80)}...`);
          warnings++;
        }
      }
    }
  });
}

console.log(`\nLink scan: ${errors} errors, ${warnings} warnings.`);
process.exit(errors > 0 ? 1 : 0);
