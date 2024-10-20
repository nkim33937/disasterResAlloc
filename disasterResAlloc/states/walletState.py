import reflex as rx
from ..components.wallet import create_multiple_wallets  # Import the async wallet function

#with just a single wallet
# class WalletState(rx.State):
#     """State to manage wallet creation and store the address."""
#     wallet_address: str = "Your wallet address will be displayed here."

#     async def generate_wallet(self):
#         """Asynchronous method to create a wallet and update state."""
#         address = await create_wallet()
#         self.wallet_address = f"Wallet created: {address}"



class WalletState(rx.State):
    """State to manage wallet creation and store the addresses."""
    wallet_addresses: list[str] = []
    status_message: str = "Click to create wallets."

    async def generate_wallets(self, num_wallets: int = 1):
        """Asynchronous method to create multiple wallets and update state."""
        self.status_message = f"Creating {num_wallets} wallet(s)..."
        try:
            new_wallets = await create_multiple_wallets(num_wallets)
            self.wallet_addresses = [wallet['classicAddress'] for wallet in new_wallets]
            self.status_message = f"Successfully created {len(self.wallet_addresses)} wallet(s)."
        except Exception as e:
            self.status_message = f"Error creating wallets: {str(e)}"

    def clear_wallets(self):
        """Clear the list of wallet addresses."""
        self.wallet_addresses = []
        self.status_message = "Wallets cleared. Click to create new ones."