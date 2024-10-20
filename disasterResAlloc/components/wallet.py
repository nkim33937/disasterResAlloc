# my_xrpl_wallet_app/pages/wallet.py
import reflex as rx
from xrpl.wallet import generate_faucet_wallet
import httpx  # An async HTTP client

FAUCET_URL = "https://faucet.altnet.rippletest.net/accounts"


wallets = []
##########with just a single wallet######
# async def create_wallet():
#     """Create an XRPL wallet using a direct faucet API call."""
#     async with httpx.AsyncClient() as client:
#         response = await client.post(FAUCET_URL)
#         response_data = response.json()

#         if response.status_code == 200:
#             wallet_address = response_data["account"]["classicAddress"]
#             print(f"Wallet created: {wallet_address}")
#             return wallet_address
#         else:
#             raise Exception("Failed to create wallet: ", response_data)

async def create_multiple_wallets(num_wallets=1):
    """Create one or more XRPL wallets using direct faucet API calls."""
    async with httpx.AsyncClient() as client:
        for _ in range(num_wallets):
            wallet = await create_single_wallet(client)
            if wallet:
                wallets.append(wallet)

    return wallets

async def create_single_wallet(client):
    """Create an XRPL wallet using a direct faucet API call."""
    response = await client.post(FAUCET_URL)
    response_data = response.json()

    if response.status_code == 200:
        wallet = response_data["account"]
        print(f"Wallet created: {wallet['classicAddress']}")
        return wallet
    else:
        raise Exception("Failed to create wallet: ", response_data)
