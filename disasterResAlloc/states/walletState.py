import reflex as rx
from ..components.wallet import create_multiple_wallets, send_xrp  # Import the async wallet function

#with just a single wallet
# class WalletState(rx.State):
#     """State to manage wallet creation and store the address."""
#     wallet_address: str = "Your wallet address will be displayed here."

#     async def generate_wallet(self):
#         """Asynchronous method to create a wallet and update state."""
#         address = await create_wallet()
#         self.wallet_address = f"Wallet created: {address}"



class WalletState(rx.State):
    wallet_addresses: list[str] = []
    wallet_seeds: list[str] = []  # Store seeds securely
    status_message: str = "Click to create wallets."
    num_wallets: int = 1

    def set_num_wallets(self, value: str):
        self.num_wallets = int(value) if value and value.isdigit() else 1

    async def generate_wallets(self):
        self.status_message = f"Creating {self.num_wallets} wallet(s)..."
        try:
            new_wallets = await create_multiple_wallets(self.num_wallets)
            self.wallet_addresses = [wallet['classicAddress'] for wallet in new_wallets]
            self.wallet_seeds = [wallet['seed'] for wallet in new_wallets]  # Store seeds securely
            self.status_message = f"Successfully created {len(self.wallet_addresses)} wallet(s)."
        except Exception as e:
            self.status_message = f"Error creating wallets: {str(e)}"

    def clear_wallets(self):
        self.wallet_addresses = []
        self.wallet_seeds = []
        self.status_message = "Wallets cleared. Click to create new ones."

    async def send_xrp_between_wallets(self, sender_index: str, receiver_index: str, amount: str):
        try:
            sender_index = int(sender_index)
            receiver_index = int(receiver_index)
            amount = float(amount)
            if sender_index >= len(self.wallet_seeds) or receiver_index >= len(self.wallet_addresses):
                self.status_message = "Invalid wallet indices."
                return

            sender_seed = self.wallet_seeds[sender_index]
            receiver_address = self.wallet_addresses[receiver_index]

            try:
                result = await send_xrp(sender_seed, receiver_address, str(amount))
                self.status_message = f"Successfully sent {amount} XRP from wallet {sender_index} to wallet {receiver_index}."
            except Exception as e:
                self.status_message = f"Error sending XRP: {str(e)}"
        except ValueError as e:
            self.status_message = f"Error: Invalid input"


