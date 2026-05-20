"use client";

import Link from "next/link";
import { ConnectButton } from "@rainbow-me/rainbowkit";

export function Header() {
  return (
    <header
      className="sticky top-0 z-40 w-full border-b border-line bg-bg/80 backdrop-blur"
      role="banner"
    >
      <a
        href="#mint"
        className="sr-only focus:not-sr-only focus:fixed focus:left-2 focus:top-2 focus:z-50 focus:rounded focus:bg-accent focus:px-3 focus:py-2 focus:text-bg"
      >
        Skip to mint
      </a>
      <div className="mx-auto flex max-w-6xl items-center justify-between px-4 py-4 sm:px-6">
        <Link
          href="/"
          className="flex items-center gap-2 font-mono text-xs font-bold uppercase tracking-[0.18em] text-white"
        >
          <img
            src="https://www.braintrust.dev/icon180.png"
            alt="Braintrust"
            width={22}
            height={22}
          />
          <span className="hidden sm:inline">Braintrust Collection</span>
        </Link>
        <nav
          aria-label="Main"
          className="hidden gap-6 font-mono text-[10px] uppercase tracking-[0.2em] text-muted md:flex"
        >
          <Link href="/" className="hover:text-white">Mint</Link>
          <Link href="/gallery" className="hover:text-white">Gallery</Link>
          <Link href="/faq" className="hover:text-white">FAQ</Link>
          <Link href="/terms" className="hover:text-white">Terms</Link>
        </nav>
        <ConnectButton
          chainStatus="icon"
          accountStatus={{ smallScreen: "avatar", largeScreen: "full" }}
          showBalance={false}
        />
      </div>
    </header>
  );
}
