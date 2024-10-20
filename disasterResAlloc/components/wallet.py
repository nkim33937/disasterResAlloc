# # my_xrpl_wallet_app/pages/wallet.py
# # import reflex as rx
# from decimal import Decimal
# # from xrpl.wallet import generate_faucet_wallet
# import httpx  # An async HTTP client
# from xrpl.models.transactions import Payment
# from xrpl.clients import JsonRpcClient
# from xrpl.transaction import submit_and_wait
# from xrpl.wallet import Wallet
# from xrpl.utils import xrp_to_drops

# FAUCET_URL = "https://faucet.altnet.rippletest.net/accounts"
# TESTNET_URL = "https://s.altnet.rippletest.net:51234"

# wallets = []
# ##########with just a single wallet######
# # async def create_wallet():
# #     """Create an XRPL wallet using a direct faucet API call."""
# #     async with httpx.AsyncClient() as client:
# #         response = await client.post(FAUCET_URL)
# #         response_data = response.json()

# #         if response.status_code == 200:
# #             wallet_address = response_data["account"]["classicAddress"]
# #             print(f"Wallet created: {wallet_address}")
# #             return wallet_address
# #         else:
# #             raise Exception("Failed to create wallet: ", response_data)

# async def create_multiple_wallets(num_wallets=1):
#     """Create one or more XRPL wallets using direct faucet API calls."""
#     async with httpx.AsyncClient() as client:
#         for _ in range(num_wallets):
#             wallet = await create_single_wallet(client)
#             if wallet:
#                 wallets.append(wallet)

#     return wallets

# # async def create_single_wallet(client):
# #     """Create an XRPL wallet using a direct faucet API call."""
# #     response = await client.post(FAUCET_URL)
# #     response_data = response.json()

# #     if response.status_code == 200:
# #         wallet = {
# #             'classicAddress': response_data['account']['classicAddress'],
# #             'seed': response_data['account']['secret']
# #         }
# #         print(f"Wallet created: {wallet['classicAddress']}")
# #         return wallet
# #     else:
# #         raise Exception("Failed to create wallet: ", response_data)
# async def create_single_wallet(client):
#     """Create an XRPL wallet using a direct faucet API call."""
#     response = await client.post(FAUCET_URL)
#     response_data = response.json()

#     print("Full response data:", response_data)  # Debug print

#     if response.status_code == 200:
        
#         account = response_data.get('account', {})
#         print("Account data:", account)  # Debug print

#         wallet = {
#             # 'classicAddress': account.get('classicAddress'),
#             # # 'seed': account.get('secret') or account.get('seed')
#             # 'seed': account[]
#             'classicAddress': account['classicAddress'],
#             'seed': response_data['seed']
#         }
        
#         print("Created wallet:", wallet)  # Debug print

#         if not wallet['classicAddress'] or not wallet['seed']:
#             raise Exception(f"Incomplete wallet data: {wallet}")

#         print(f"Wallet created: {wallet['classicAddress']}")
#         return wallet
#     else:
#         raise Exception("Failed to create wallet: ", response_data)

# async def send_xrp(sender_seed: str, destination_address: str, amount: str):
#     """
#     Send XRP from one wallet to another.
    
#     :param sender_seed: The seed of the sending wallet
#     :param destination_address: The address of the receiving wallet
#     :param amount: The amount of XRP to send (as a string)
#     :return: The result of the transaction
#     """
#     client = JsonRpcClient(TESTNET_URL)
#     sender_wallet = Wallet.from_seed(sender_seed)

#     payment = Payment(
#         account=sender_wallet.classic_address,
#         amount=xrp_to_drops(Decimal(amount)),
#         destination=destination_address,
#     )

#     # signed_tx = safe_sign_and_autofill_transaction(payment, sender_wallet, client)
#     # tx_response = send_reliable_submission(signed_tx, client)

#     # return tx_response.result
#     # Sign and submit the transaction
#     try:
#         response = await submit_and_wait(payment, client, sender_wallet)
#         print("Transaction result:", response.result)  # Debug print
#         return response.result
#     except Exception as e:
#         print(f"Transaction failed: {str(e)}")  # Debug print
#         return f"Transaction failed: {str(e)}"
    

# # import asyncio
# async def test_send_xrp():
#     print("Starting test_send_xrp function...")
#     print("Creating wallets...")

#     # Step 1: Create two wallets
#     created_wallets = await create_multiple_wallets(2)

#     # Ensure we have at least two wallets
#     if len(created_wallets) < 2:
#         print("Error: Failed to create wallets.")
#         return

#     sender_seed = created_wallets[0]['seed']
#     receiver_address = created_wallets[1]['classicAddress']

#     print(f"Sender seed: {sender_seed}")
#     print(f"Receiver address: {receiver_address}")

#     # Step 2: Send XRP from one wallet to another
#     amount = "10"  # Specify amount to send (in XRP)
#     print(f"Attempting to send {amount} XRP...")
#     try:
#         result = await send_xrp(sender_seed, receiver_address, amount)
#         print(f"Send XRP result: {result}")
#     except Exception as e:
#         print(f"Exception in send_xrp: {str(e)}")
#         return

#     # Step 3: Check result
#     if isinstance(result, dict) and 'engine_result' in result and result['engine_result'] == 'tesSUCCESS':
#         print(f"Successfully sent {amount} XRP from wallet 0 to wallet 1.")
#     else:
#         print(f"Failed to send XRP: {result}")

#     print("test_send_xrp function completed.")

# if __name__ == "__main__":
#     import asyncio
#     asyncio.run(test_send_xrp())



# my_xrpl_wallet_app/pages/wallet.py
from decimal import Decimal
import httpx  # An async HTTP client
from xrpl.models.transactions import Payment
from xrpl.asyncio.clients import AsyncJsonRpcClient
from xrpl.asyncio.transaction import submit_and_wait
from xrpl.wallet import Wallet
from xrpl.utils import xrp_to_drops

FAUCET_URL = "https://faucet.altnet.rippletest.net/accounts"
TESTNET_URL = "https://s.altnet.rippletest.net:51234"

async def create_multiple_wallets(num_wallets=1):
    """Create one or more XRPL wallets using direct faucet API calls."""
    wallets = []  # Use a local list to avoid global state
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

    print("Full response data:", response_data)  # Debug print

    if response.status_code == 200:
        account = response_data.get('account', {})
        print("Account data:", account)  # Debug print

        wallet = {
            'classicAddress': account.get('classicAddress'),
            'seed': response_data.get('seed')  # Corrected line
        }

        if not wallet['classicAddress'] or not wallet['seed']:
            raise Exception(f"Incomplete wallet data: {wallet}")

        print(f"Wallet created: {wallet['classicAddress']}")
        return wallet
    else:
        raise Exception(f"Failed to create wallet: {response_data}")

async def send_xrp(sender_seed: str, destination_address: str, amount):
    """
    Send XRP from one wallet to another asynchronously.

    :param sender_seed: The seed of the sending wallet
    :param destination_address: The address of the receiving wallet
    :param amount: The amount of XRP to send (as a Decimal or int)
    :return: The result of the transaction
    """
    client = AsyncJsonRpcClient(TESTNET_URL)
    sender_wallet = Wallet.from_seed(sender_seed)

    # Ensure amount is a Decimal
    if not isinstance(amount, (Decimal, int)):
        amount = Decimal(amount)

    payment = Payment(
        account=sender_wallet.classic_address,
        amount=xrp_to_drops(amount),
        destination=destination_address,
    )

    try:
        response = await submit_and_wait(payment, client, sender_wallet)
        print("Transaction result:", response.result)  # Debug print
        return response.result
    except Exception as e:
        print(f"Transaction failed: {str(e)}")  # Debug print
        return f"Transaction failed: {str(e)}"
    # Remove the finally block since there's no close() method


# async def test_send_xrp():
#     print("Starting test_send_xrp function...")
#     print("Creating wallets...")

#     # Step 1: Create two wallets
#     try:
#         created_wallets = await create_multiple_wallets(2)
#     except Exception as e:
#         print(f"Error creating wallets: {str(e)}")
#         return

#     # Ensure we have at least two wallets
#     if len(created_wallets) < 2:
#         print("Error: Failed to create wallets.")
#         return

#     sender_seed = created_wallets[0]['seed']
#     receiver_address = created_wallets[1]['classicAddress']

#     print(f"Sender seed: {sender_seed}")
#     print(f"Receiver address: {receiver_address}")

#     # Step 2: Send XRP from one wallet to another
#     amount = "10"  # Specify amount to send (in XRP)
#     print(f"Attempting to send {amount} XRP...")
#     try:
#         result = await send_xrp(sender_seed, receiver_address, amount)
#         print(f"Send XRP result: {result}")
#     except Exception as e:
#         print(f"Exception in send_xrp: {str(e)}")
#         return

#     # Step 3: Check result
#     if isinstance(result, dict) and result.get('engine_result') == 'tesSUCCESS':
#         print(f"Successfully sent {amount} XRP from wallet 0 to wallet 1.")
#     else:
#         print(f"Failed to send XRP: {result}")

#     print("test_send_xrp function completed.")

# if __name__ == "__main__":
#     import asyncio
#     asyncio.run(test_send_xrp())
