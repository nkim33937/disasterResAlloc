# import reflex as rx
# from ..components.wallet import create_wallet  # Use relative import
# import asyncio
# @rx.page(route="/wallet", title="Wallet")
# def WalletPage() -> rx.Component:
#     def handle_create_wallet():
#         if asyncio.iscoroutinefunction(create_wallet):
#             # If create_wallet is a coroutine function, use await
#             # wallet = asyncio.run(create_wallet())
#             return rx.text(f"Wallet created:")
#         # Try to get the running loop and use create_task()
#         loop = asyncio.get_running_loop()
#         loop.create_task(create_wallet())

            
#     # Create a simple button to trigger wallet creation
#     return rx.container(
#         rx.button("Create Wallet", on_click=handle_create_wallet),
#         rx.text("Your wallet address will be displayed here after creation.")
#     )

import reflex as rx
from ..states.walletState import WalletState  # Import the state

@rx.page(route="/wallet", title="Wallet")
def WalletPage() -> rx.Component:
    """Page to generate and display an XRPL wallet address."""
    return rx.container(
        rx.button(
            "Create Wallet", 
            on_click=WalletState.generate_wallet  # Call the async method on click
        ),
        rx.text(WalletState.wallet_address),  # Display the wallet address from state
        padding="20px",
        border="1px solid #ddd",
        border_radius="8px"
    )
