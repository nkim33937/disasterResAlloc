# import sys
# import os

# # Add the parent directory of 'disasterResAlloc' to the Python path
# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import reflex as rx
from ..components.wallet import create_multiple_wallets, send_xrp
# from disasterResAlloc.disasterResAlloc.components.wallet import create_multiple_wallets, send_xrp
#with just a single wallet
# class WalletState(rx.State):
#     """State to manage wallet creation and store the address."""
#     wallet_address: str = "Your wallet address will be displayed here."

#     async def generate_wallet(self):
#         """Asynchronous method to create a wallet and update state."""
#         address = await create_wallet()
#         self.wallet_address = f"Wallet created: {address}"



# class WalletState(rx.State):
#     wallet_addresses: list[str] = []
#     wallet_seeds: list[str] = []  # Store seeds securely
#     status_message: str = "Click to create wallets."
#     num_wallets: int = 1

#     def set_num_wallets(self, value: str):
#         self.num_wallets = int(value) if value and value.isdigit() else 1

#     async def generate_wallets(self):
#         self.status_message = f"Creating {self.num_wallets} wallet(s)..."
#         try:
#             new_wallets = await create_multiple_wallets(self.num_wallets)
#             self.wallet_addresses = [wallet['classicAddress'] for wallet in new_wallets]
#             self.wallet_seeds = [wallet['seed'] for wallet in new_wallets]  # Store seeds securely
#             self.status_message = f"Successfully created {len(self.wallet_addresses)} wallet(s)."
#         except Exception as e:
#             self.status_message = f"Error creating wallets: {str(e)}"

#     def clear_wallets(self):
#         self.wallet_addresses = []
#         self.wallet_seeds = []
#         self.status_message = "Wallets cleared. Click to create new ones."

#     async def send_xrp_between_wallets(self, sender_index: str, receiver_index: str, amount: str):
#         try:
#             print("sender_index", sender_index)
#             print("receiver_index", receiver_index)
#             print("amount", amount)
#             sender_index = int(sender_index)
#             receiver_index = int(receiver_index)
#             amount = float(amount)
#             if sender_index >= len(self.wallet_seeds) or receiver_index >= len(self.wallet_addresses):
#                 self.status_message = "Invalid wallet indices."
#                 return

#             sender_seed = self.wallet_seeds[sender_index]
#             receiver_address = self.wallet_addresses[receiver_index]

#             try:
#                 result = await send_xrp(sender_seed, receiver_address, str(amount))
#                 self.status_message = f"Successfully sent {amount} XRP from wallet {sender_index} to wallet {receiver_index}."
#             except Exception as e:
#                 self.status_message = f"Error sending XRP: {str(e)}"
#         except ValueError as e:
#             self.status_message = f"Error: Invalid input"

class WalletState(rx.State):
    # Existing state variables...
    wallet_addresses: list[str] = []
    wallet_seeds: list[str] = []  # Store seeds securely
    status_message: str = "Click to create wallets."
    num_wallets: int = 1

    # New state variables for transferring XRP
    sender_index: int = 0
    receiver_index: int = 0
    amount: float = 0.0

    # Method to set the sender index
    def set_sender_index(self, value: str):
        try:
            self.sender_index = int(value)
        except ValueError:
            self.status_message = "Invalid sender index."

    # Method to set the receiver index
    def set_receiver_index(self, value: str):
        try:
            self.receiver_index = int(value)
        except ValueError:
            self.status_message = "Invalid receiver index."

    # Method to set the amount
    def set_amount(self, value: str):
        try:
            self.amount = float(value)
        except ValueError:
            self.status_message = "Invalid amount."

    # Implemented generate_wallets method
    async def generate_wallets(self):
        self.status_message = f"Creating {self.num_wallets} wallet(s)..."
        try:
            print(f"Attempting to create {self.num_wallets} wallet(s)")
            new_wallets = await create_multiple_wallets(self.num_wallets)
            print(f"Received new wallets: {new_wallets}")

            self.wallet_addresses = [wallet['classicAddress'] for wallet in new_wallets]
            self.wallet_seeds = [wallet['seed'] for wallet in new_wallets]

            print(f"Wallet Addresses: {self.wallet_addresses}")
            print(f"Wallet Seeds: {self.wallet_seeds}")

            self.status_message = f"Successfully created {len(self.wallet_addresses)} wallet(s)."
        except Exception as e:
            self.status_message = f"Error creating wallets: {str(e)}"
            print(f"Exception in generate_wallets: {e}")

    def clear_wallets(self):
        self.wallet_addresses = []
        self.wallet_seeds = []
        self.status_message = "Wallets cleared."

    # Method to send XRP between wallets
    async def send_xrp_between_wallets(self):
        num_wallets = len(self.wallet_addresses)
        if not (0 <= self.sender_index < num_wallets) or not (0 <= self.receiver_index < num_wallets):
            self.status_message = "Invalid wallet indices."
            return

        if self.sender_index == self.receiver_index:
            self.status_message = "Cannot send XRP to the same wallet."
            return

        sender_seed = self.wallet_seeds[self.sender_index]
        receiver_address = self.wallet_addresses[self.receiver_index]

        print(f"Sender Index: {self.sender_index}")
        print(f"Receiver Index: {self.receiver_index}")
        print(f"Sender Seed: {sender_seed}")
        print(f"Receiver Address: {receiver_address}")
        print(f"Amount: {self.amount}")

        result = await send_xrp(sender_seed, receiver_address, self.amount)

        # Correctly interpret the transaction result
        if isinstance(result, dict):
            transaction_result = result.get('meta', {}).get('TransactionResult')
            if transaction_result == 'tesSUCCESS':
                self.status_message = (
                    f"Sent {self.amount} XRP from wallet {self.sender_index} to wallet {self.receiver_index}"
                )
            else:
                self.status_message = f"Failed to send XRP: {transaction_result}"
                print(f"Send XRP Failed: {transaction_result}")
        else:
            self.status_message = f"Failed to send XRP: {result}"
            print(f"Send XRP Failed: {result}")

