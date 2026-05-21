// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

/**
 * LocalMockDrop (v2)
 *
 * Local-only mock used for testing the wallet-bound 3-variant mint flow.
 * Supply: 15 SDRs x 3 variants = 45 tokens.
 * Each wallet on the allowlist is bound to exactly one SDR (slug index).
 * That wallet can mint up to 3 tokens, and each mint returns the next
 * sequential variant of that wallet's SDR (no other SDR is reachable from
 * this wallet).
 *
 * Token layout:
 *   slug index 0  -> tokens 0, 1, 2
 *   slug index 1  -> tokens 3, 4, 5
 *   ...
 *   slug index 14 -> tokens 42, 43, 44
 *
 * This logic does NOT exist in thirdweb's DropERC721. Production deployment
 * (Sepolia or mainnet) will need either a custom ERC721 with the same rules,
 * or thirdweb claim conditions split into 15 per-SDR allowlisted phases.
 * This contract is for local frontend testing ONLY. Not audited. Not for
 * production.
 *
 * The claim() signature still mirrors thirdweb's so the MintCard frontend
 * works unchanged. The receiver/quantity/value enforcement plus the
 * wallet-to-SDR binding all live in this contract.
 */
import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/utils/Strings.sol";

contract LocalMockDrop is ERC721, Ownable {
    using Strings for uint256;

    // ====== Constants ======
    uint256 public constant VARIANTS_PER_SDR = 3;
    uint256 public constant SDR_COUNT = 15;
    uint256 public constant MAX_PER_WALLET = 3;
    // Slug indices are stored 1-based so 0 acts as "not allowlisted".

    address public constant NATIVE_TOKEN =
        0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE;

    // ====== Storage ======
    string private _baseUriValue;
    uint256 public totalMinted;
    bool private _paused;

    // wallet -> 1-based slug index (1..15). 0 means "not on allowlist".
    mapping(address => uint256) public walletSlugIndex;
    // wallet -> count of variants already claimed (0..3).
    mapping(address => uint256) public walletClaimedCount;

    // ====== thirdweb-compatible claim condition (purely informational) ======
    struct ClaimCondition {
        uint256 startTimestamp;
        uint256 maxClaimableSupply;
        uint256 supplyClaimed;
        uint256 quantityLimitPerWallet;
        bytes32 merkleRoot;
        uint256 pricePerToken;
        address currency;
        string metadata;
    }
    struct AllowlistProof {
        bytes32[] proof;
        uint256 quantityLimitPerWallet;
        uint256 pricePerToken;
        address currency;
    }
    ClaimCondition private _condition;

    // ====== Events ======
    event Claimed(address indexed receiver, uint256 startTokenId, uint256 quantity);
    event AllowlistSet(address indexed wallet, uint256 slugIndex1Based);

    constructor(string memory name_, string memory symbol_)
        ERC721(name_, symbol_)
        Ownable(msg.sender)
    {
        _condition = ClaimCondition({
            startTimestamp: block.timestamp,
            maxClaimableSupply: SDR_COUNT * VARIANTS_PER_SDR,
            supplyClaimed: 0,
            quantityLimitPerWallet: MAX_PER_WALLET,
            merkleRoot: bytes32(0),
            pricePerToken: 0,
            currency: NATIVE_TOKEN,
            metadata: "local-mock-v2"
        });
    }

    // ====== Owner ======
    function setBaseURI(string calldata uri) external onlyOwner {
        _baseUriValue = uri;
    }

    function setPaused(bool p) external onlyOwner {
        _paused = p;
    }

    function setAllowlistEntry(address wallet, uint256 slugIndex1Based) external onlyOwner {
        require(slugIndex1Based <= SDR_COUNT, "BadSlugIndex");
        walletSlugIndex[wallet] = slugIndex1Based;
        emit AllowlistSet(wallet, slugIndex1Based);
    }

    function setAllowlistBatch(
        address[] calldata wallets,
        uint256[] calldata slugIndices1Based
    ) external onlyOwner {
        require(wallets.length == slugIndices1Based.length, "LengthMismatch");
        for (uint256 i = 0; i < wallets.length; i++) {
            require(slugIndices1Based[i] <= SDR_COUNT, "BadSlugIndex");
            walletSlugIndex[wallets[i]] = slugIndices1Based[i];
            emit AllowlistSet(wallets[i], slugIndices1Based[i]);
        }
    }

    // ====== Reads ======
    function paused() external view returns (bool) {
        return _paused;
    }

    function maxTotalSupply() external pure returns (uint256) {
        return SDR_COUNT * VARIANTS_PER_SDR;
    }

    function nextTokenIdToMint() external view returns (uint256) {
        // Returns total minted count, used by frontend "minted / maxSupply" display.
        return totalMinted;
    }

    function maxClaimableSupply() external pure returns (uint256) {
        return SDR_COUNT * VARIANTS_PER_SDR;
    }

    function getActiveClaimConditionId() external pure returns (uint256) {
        return 0;
    }

    function getClaimConditionById(uint256)
        external
        view
        returns (ClaimCondition memory)
    {
        return _condition;
    }

    function isAllowlisted(address wallet) external view returns (bool) {
        return walletSlugIndex[wallet] > 0;
    }

    function slugIndexFor(address wallet) external view returns (uint256) {
        // Returns 0 if not allowlisted, else 1..15.
        return walletSlugIndex[wallet];
    }

    function remainingForWallet(address wallet) external view returns (uint256) {
        uint256 claimed = walletClaimedCount[wallet];
        return claimed >= MAX_PER_WALLET ? 0 : MAX_PER_WALLET - claimed;
    }

    function _baseURI() internal view override returns (string memory) {
        return _baseUriValue;
    }

    function tokenURI(uint256 tokenId) public view override returns (string memory) {
        _requireOwned(tokenId);
        string memory base = _baseURI();
        return bytes(base).length > 0
            ? string(abi.encodePacked(base, tokenId.toString(), ".json"))
            : "";
    }

    // ====== Claim ======
    function claim(
        address receiver,
        uint256 quantity,
        address /*currency*/,
        uint256 /*pricePerToken*/,
        AllowlistProof calldata /*allowlistProof*/,
        bytes calldata /*data*/
    ) external payable {
        require(!_paused, "DropPaused");
        require(quantity > 0, "DropBadQuantity");
        require(msg.value == 0, "DropFreeClaimOnly");

        uint256 slugIdx1 = walletSlugIndex[receiver];
        require(slugIdx1 > 0, "NotAllowlisted");
        // Convert to 0-based.
        uint256 slugIdx = slugIdx1 - 1;

        uint256 alreadyClaimed = walletClaimedCount[receiver];
        require(alreadyClaimed + quantity <= MAX_PER_WALLET, "DropClaimExceedLimit");

        // Token id for this wallet's k-th claim is slugIdx * 3 + k (0-indexed).
        uint256 startTokenId = slugIdx * VARIANTS_PER_SDR + alreadyClaimed;
        for (uint256 i = 0; i < quantity; i++) {
            _safeMint(receiver, startTokenId + i);
        }

        walletClaimedCount[receiver] = alreadyClaimed + quantity;
        totalMinted += quantity;
        _condition.supplyClaimed += quantity;

        emit Claimed(receiver, startTokenId, quantity);
    }
}
