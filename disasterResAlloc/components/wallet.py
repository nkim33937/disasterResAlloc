# my_xrpl_wallet_app/pages/wallet.py
import reflex as rx
import xrpl
from xrpl.wallet import generate_faucet_wallet

def create_wallet():
    client = xrpl.clients.JsonRpcClient("https://s.altnet.rippletest.net:51234")
    
    # Create a new wallet asynchronously
    wallet = await generate_faucet_wallet(client)  # Use await instead of asyncio.run()
    
    return wallet