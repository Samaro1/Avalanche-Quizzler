import { ethers } from "ethers";

/**
 * Trims a wallet address to a shorter format, e.g., "0x1234...5678".
 * @param {string} address The full wallet address.
 * @returns {string} The trimmed address.
 */
function trimAddress(address) {
  if (!address) return "";
  return `${address.substring(0, 6)}...${address.substring(address.length - 4)}`;
}
const FUJI_CHAIN_ID = 43113; // Avalanche Fuji Testnet chain ID
const FUJI_CHAIN_ID_HEX = '0xA869'; // 43113 in hex

async function connectWallet() {
  if (!window.ethereum) {
    alert("MetaMask is not installed!"); //check if MetaMask is installed
    return;
  }
  const provider = new ethers.providers.Web3Provider(window.ethereum);

  // Check if the user is on the correct network and prompt them to switch if not
  const { chainId } = await provider.getNetwork();
  if (chainId !== FUJI_CHAIN_ID) {
    try {
      await window.ethereum.request({
        method: 'wallet_switchEthereumChain',
        params: [{ chainId: FUJI_CHAIN_ID_HEX }],
      });
    } catch (switchError) {
      // This error code indicates that the chain has not been added to MetaMask.
      if (switchError.code === 4902) {
        try {
          await window.ethereum.request({
            method: 'wallet_addEthereumChain',
            params: [
              {
                chainId: FUJI_CHAIN_ID_HEX,
                chainName: 'Avalanche Fuji Testnet',
                nativeCurrency: { name: 'AVAX', symbol: 'AVAX', decimals: 18 },
                rpcUrls: ['https://api.avax-test.network/ext/bc/C/rpc'],
                blockExplorerUrls: ['https://testnet.snowtrace.io/'],
              },
            ],
          });
        } catch (addError) {
          console.error("Failed to add the Fuji network:", addError);
          alert("Failed to add the Fuji network. Please add it manually in MetaMask.");
          return;
        }
      } else {
        console.error("Failed to switch network:", switchError);
        alert("Could not switch to the Fuji network. Please do it manually in MetaMask.");
        return;
      }
    }
  }

  try {
    await provider.send("eth_requestAccounts", []);
    const signer = provider.getSigner();

    //set wallet address
    const walletAddress = document.getElementById("walletAddress");
    const fullAddress = await signer.getAddress();
    walletAddress.innerText = `Connected: ${trimAddress(fullAddress)}`;
    console.log("Wallet connected.");
  } catch (error) {
    console.error("Failed to connect wallet:", error);
    alert("Failed to connect wallet. Check console for details.");
  }
}

document.getElementById("connectButton").addEventListener("click", connectWallet);