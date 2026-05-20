/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  // SVGs are served as static assets from /public, including all existing artwork.
  // Do not touch public/nfts/, public/sdrs/, public/photos/.
  webpack: (config) => {
    // wagmi/viem need this for some optional deps
    config.externals.push('pino-pretty', 'lokijs', 'encoding');
    return config;
  },
};

module.exports = nextConfig;
