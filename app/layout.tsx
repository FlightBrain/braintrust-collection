import "./globals.css";
import type { Metadata } from "next";
import { Providers } from "./providers";

export const metadata: Metadata = {
  title: "Braintrust Collection · Genesis Mint",
  description:
    "15 hand-pixeled collectible cards. The Sales Floor Genesis drop. Mint on Base.",
  icons: { icon: "https://www.braintrust.dev/icon180.png" },
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>
        <Providers>{children}</Providers>
      </body>
    </html>
  );
}
