/**
 * Authoritative SDR slug order. Must match public/auto_people.json AND
 * scripts/deploy-local-contract.ts -> SDR_SLUG_TO_INDEX1.
 *
 * Used by the frontend to translate the on-chain `slugIndexFor(wallet)`
 * read into a human-readable coworker name.
 */
export const SDR_SLUG_ORDER = [
  "alec",
  "ava",
  "catherine",
  "chris",
  "duncan",
  "evan",
  "garrett",
  "joe",
  "kensington",
  "keslar",
  "nick",
  "owen",
  "ryan",
  "sacha",
  "shaune",
] as const;

export type SdrSlug = (typeof SDR_SLUG_ORDER)[number];

export const SDR_NAMES: Record<SdrSlug, string> = {
  alec: "Alec Sloan",
  ava: "Ava Baker",
  catherine: "Catherine Vincent",
  chris: "Chris Koenig",
  duncan: "Duncan Lewis",
  evan: "Evan O'Reilly",
  garrett: "Garrett Buchanan",
  joe: "Joe Meade",
  kensington: "Kensington Belza",
  keslar: "Keslar Simpson",
  nick: "Nick Gaspardone",
  owen: "Owen Bloomer",
  ryan: "Ryan Gwyn",
  sacha: "Sacha Thompson",
  shaune: "Shaune Lundstrom",
};

export function slugForIndex1Based(idx1: number): SdrSlug | null {
  if (idx1 < 1 || idx1 > SDR_SLUG_ORDER.length) return null;
  return SDR_SLUG_ORDER[idx1 - 1];
}
