// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

/**
 * LocalMockDrop
 *
 * A minimal mock of thirdweb's DropERC721 used ONLY on a local Hardhat node
 * for frontend testing. It is NOT production-grade and must never be deployed
 * to mainnet. The ABI is intentionally shaped to match thirdweb's
 * `claim(receiver, quantity, currency, pricePerToken, AllowlistProof, data)`
 * so the existing MintCard frontend works unchanged.
 *
 * What it implements:
 *   - ERC-721 mint with token ids starting at 0
 *   - Free claim (price = 0)
 *   - Per-wallet limit (1 by default, configurable)
 *   - Hard total supply cap (default 15)
 *   - Pausable
 *   - tokenURI = baseURI + id
 *   - thirdweb-style claim condition reads
 *
 * What it does NOT implement:
 *   - Merkle allowlists (proof is accepted and ignored)
 *   - ERC-2981 royalty enforcement
 *   - Currency other than native ETH
 *   - Sale window scheduling beyond `startTimestamp`
 *   - Access control beyond a single owner
 *
 * Anyone reading this contract for production use: stop. Use thirdweb's real
 * DropERC721 or an audited OpenZeppelin-based contract.
 */
import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/utils/Strings.sol";

contract LocalMockDrop is ERC721, Ownable {
    using Strings for uint256;

    // ====== Storage ======
    string private _baseUriValue;
    uint256 public nextTokenIdToMint;   // doubles as supply-claimed count
    uint256 public maxTotalSupply;
    bool private _paused;

    // ====== thirdweb-compatible claim condition ======
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
    mapping(address => uint256) public claimedPerWallet;

    address public constant NATIVE_TOKEN =
        0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE;

    // ====== Events ======
    event Claimed(address indexed receiver, uint256 startTokenId, uint256 quantity);

    constructor(
        string memory name_,
        string memory symbol_,
        uint256 maxSupply_
    ) ERC721(name_, symbol_) Ownable(msg.sender) {
        maxTotalSupply = maxSupply_;
        _condition = ClaimCondition({
            startTimestamp: block.timestamp,
            maxClaimableSupply: maxSupply_,
            supplyClaimed: 0,
            quantityLimitPerWallet: 1,
            merkleRoot: bytes32(0),
            pricePerToken: 0,
            currency: NATIVE_TOKEN,
            metadata: "local-mock"
        });
    }

    // ====== Owner ======
    function setBaseURI(string calldata uri) external onlyOwner {
        _baseUriValue = uri;
    }

    function setPaused(bool p) external onlyOwner {
        _paused = p;
    }

    function setMaxPerWallet(uint256 n) external onlyOwner {
        _condition.quantityLimitPerWallet = n;
    }

    // ====== Reads (thirdweb-compatible names) ======
    function paused() external view returns (bool) {
        return _paused;
    }

    function maxClaimableSupply() external view returns (uint256) {
        return maxTotalSupply;
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
        require(
            nextTokenIdToMint + quantity <= maxTotalSupply,
            "DropClaimExceedMaxSupply"
        );
        require(
            claimedPerWallet[receiver] + quantity <= _condition.quantityLimitPerWallet,
            "DropClaimExceedLimit"
        );
        // Free claim by design. Reject any sent ETH to keep behavior obvious.
        require(msg.value == 0, "DropFreeClaimOnly");

        uint256 startId = nextTokenIdToMint;
        for (uint256 i = 0; i < quantity; i++) {
            _safeMint(receiver, nextTokenIdToMint);
            unchecked { nextTokenIdToMint += 1; }
        }
        claimedPerWallet[receiver] += quantity;
        _condition.supplyClaimed += quantity;

        emit Claimed(receiver, startId, quantity);
    }
}
