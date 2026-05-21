import { HardhatUserConfig } from "hardhat/config";
import "@nomicfoundation/hardhat-toolbox";

/**
 * Hardhat config for local-only contract testing.
 *
 * - sources live in ./contracts
 * - cache + artifacts go under ./.cache so they don't pollute the repo
 * - localhost network: chain id 31337, RPC http://127.0.0.1:8545
 *
 * NEVER use the well-known Hardhat private keys for real funds. They are
 * deterministic and public.
 */
const config: HardhatUserConfig = {
  solidity: {
    version: "0.8.24",
    settings: {
      optimizer: { enabled: true, runs: 200 },
      // OpenZeppelin 5.x uses `mcopy` (Cancun opcode).
      evmVersion: "cancun",
    },
  },
  paths: {
    sources: "./contracts",
    tests: "./contracts/test",
    cache: "./.cache/hardhat-cache",
    artifacts: "./.cache/hardhat-artifacts",
  },
  networks: {
    hardhat: {
      chainId: 31337,
    },
    localhost: {
      url: "http://127.0.0.1:8545",
      chainId: 31337,
    },
  },
};

export default config;
