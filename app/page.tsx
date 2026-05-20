import { Header } from "@/components/Header";
import { Hero } from "@/components/Hero";
import { MintCard } from "@/components/MintCard";
import { SafetyBanner } from "@/components/SafetyBanner";
import { FooterNav } from "@/components/FooterNav";

export default function HomePage() {
  return (
    <main>
      <Header />
      <Hero />
      <MintCard />
      <SafetyBanner />
      <FooterNav />
    </main>
  );
}
