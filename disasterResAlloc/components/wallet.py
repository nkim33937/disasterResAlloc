# my_xrpl_wallet_app/pages/wallet.py
import reflex as rx
from xrpl.wallet import generate_faucet_wallet
import httpx  # An async HTTP client

FAUCET_URL = "https://faucet.altnet.rippletest.net/accounts"

async def create_wallet():
    """Create an XRPL wallet using a direct faucet API call."""
    async with httpx.AsyncClient() as client:
        response = await client.post(FAUCET_URL)
        response_data = response.json()

        if response.status_code == 200:
            wallet_address = response_data["account"]["classicAddress"]
            print(f"Wallet created: {wallet_address}")
            return wallet_address
        else:
            raise Exception("Failed to create wallet: ", response_data)
