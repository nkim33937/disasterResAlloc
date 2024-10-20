import reflex as rx
from ..components.wallet import create_wallet  # Import the async wallet function

class WalletState(rx.State):
    """State to manage wallet creation and store the address."""
    wallet_address: str = "Your wallet address will be displayed here."

    async def generate_wallet(self):
        """Asynchronous method to create a wallet and update state."""
        address = await create_wallet()
        self.wallet_address = f"Wallet created: {address}"
