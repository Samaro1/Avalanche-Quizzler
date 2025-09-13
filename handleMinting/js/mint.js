import { ethers } from "ethers";

const contractAddress = "0xF93b8708cf6605f945A9be9e694200fD69c7E6aA" //NFT contract address on Fuji Testnet

const contractABI = [
  "function mint(address to) public",
  "function name() view returns (string)"
]; // Simplified ABI with only the mint function and name function

async function mintNFT() {
  if (!window.ethereum) {
    alert("MetaMask is not installed!");
    return;
  }

  const provider = new ethers.providers.Web3Provider(window.ethereum);
  const signer = provider.getSigner();

  // Check if a wallet is connected
  try {
    await signer.getAddress();
  } catch (error) {
    alert("Please connect your wallet first.");
    return;
  }

  //mint nft
  console.log("Minting NFT...");

  const contract = new ethers.Contract(contractAddress, contractABI, signer);
  try {
    const userAddress = await signer.getAddress();
    const tx = await contract.mint(userAddress);
    await tx.wait();
    alert("NFT minted successfully!");
  } catch (error) {
    console.error("Error minting NFT:", error);
    alert("Error minting NFT. Check console for details.");
  }
}

document.getElementById("mintButton").addEventListener("click", mintNFT);
