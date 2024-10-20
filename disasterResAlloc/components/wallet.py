# my_xrpl_wallet_app/pages/wallet.py
import reflex as rx
# from xrpl.wallet import generate_faucet_wallet
import httpx  # An async HTTP client
from xrpl.models.transactions import Payment
from xrpl.clients import JsonRpcClient
from xrpl.transaction import submit_and_wait
from xrpl.wallet import Wallet
from xrpl.utils import xrp_to_drops

FAUCET_URL = "https://faucet.altnet.rippletest.net/accounts"
TESTNET_URL = "https://s.altnet.rippletest.net:51234"

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

# async def create_single_wallet(client):
#     """Create an XRPL wallet using a direct faucet API call."""
#     response = await client.post(FAUCET_URL)
#     response_data = response.json()

#     if response.status_code == 200:
#         wallet = {
#             'classicAddress': response_data['account']['classicAddress'],
#             'seed': response_data['account']['secret']
#         }
#         print(f"Wallet created: {wallet['classicAddress']}")
#         return wallet
#     else:
#         raise Exception("Failed to create wallet: ", response_data)
async def create_single_wallet(client):
    """Create an XRPL wallet using a direct faucet API call."""
    response = await client.post(FAUCET_URL)
    response_data = response.json()

    print("Full response data:", response_data)  # Debug print

    if response.status_code == 200:
        
        account = response_data.get('account', {})
        print("Account data:", account)  # Debug print

        wallet = {
            # 'classicAddress': account.get('classicAddress'),
            # # 'seed': account.get('secret') or account.get('seed')
            # 'seed': account[]
            'classicAddress': account['classicAddress'],
            'seed': response_data['seed']
        }
        
        print("Created wallet:", wallet)  # Debug print

        if not wallet['classicAddress'] or not wallet['seed']:
            raise Exception(f"Incomplete wallet data: {wallet}")

        print(f"Wallet created: {wallet['classicAddress']}")
        return wallet
    else:
        raise Exception("Failed to create wallet: ", response_data)

def send_xrp(sender_seed: str, destination_address: str, amount: str):
    """
    Send XRP from one wallet to another.
    
    :param sender_seed: The seed of the sending wallet
    :param destination_address: The address of the receiving wallet
    :param amount: The amount of XRP to send (as a string)
    :return: The result of the transaction
    """
    client = JsonRpcClient(TESTNET_URL)
    sender_wallet = Wallet.from_seed(sender_seed)

    payment = Payment(
        account=sender_wallet.classic_address,
        amount=xrp_to_drops(amount),
        destination=destination_address,
    )

    # signed_tx = safe_sign_and_autofill_transaction(payment, sender_wallet, client)
    # tx_response = send_reliable_submission(signed_tx, client)

    # return tx_response.result
    # Sign and submit the transaction
    try:
        response = submit_and_wait(payment, client, sender_wallet)
        return response.result
    except Exception as e:
        return f"Transaction failed: {str(e)}"
    

import asyncio

async def main():
    wallets = await create_multiple_wallets(2)
    print("Created wallets:", wallets)


if __name__ == "__main__":
    asyncio.run(main())