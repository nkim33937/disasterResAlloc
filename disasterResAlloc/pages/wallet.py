import reflex as rx
from ..components.wallet import create_wallet  # Use relative import

@rx.page(route="/wallet", title="Wallet")
def WalletPage() -> rx.Component:
    def handle_create_wallet():
        wallet = create_wallet()  # Call the wallet creation function
        print("Wallet created:", wallet.classic_address)  # Optional: print to console
        
    # Create a simple button to trigger wallet creation
    return rx.container(
        rx.button("Create Wallet", on_click=handle_create_wallet),
        rx.text("Your wallet address will be displayed here after creation.")
    )