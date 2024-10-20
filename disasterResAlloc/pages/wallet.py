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

#with single wallet
# @rx.page(route="/wallet", title="Wallet")
# def WalletPage() -> rx.Component:
#     """Page to generate and display an XRPL wallet address."""
#     return rx.container(
#         rx.button(
#             "Create Wallet", 
#             on_click=WalletState.generate_wallet  # Call the async method on click
#         ),
#         rx.text(WalletState.wallet_address),  # Display the wallet address from state
#         padding="20px",
#         border="1px solid #ddd",
#         border_radius="8px"
#     )

#with multiple wallets
def WalletPage() -> rx.Component:
    """Page to generate and display XRPL wallet addresses."""
    return rx.container(
        rx.vstack(
            rx.heading("XRPL Wallet Generator"),
            rx.input(
                placeholder="Number of wallets",
                type="number",
                min=1,
                max=10,
                value=1,
                id="num_wallets"
            ),
            rx.button(
                "Create Wallets", 
                on_click=lambda: WalletState.generate_wallets(5)
            ),
            rx.button(
                "Clear Wallets",
                on_click=WalletState.clear_wallets
            ),
            rx.text(WalletState.status_message),
            rx.ordered_list(
                rx.foreach(
                    WalletState.wallet_addresses,
                    lambda address: rx.list_item(address)
                )
            ),
            spacing="4",
            align_items="start",
        ),
        max_width="800px",
        margin="0 auto",
        padding="20px",
        border="1px solid #ddd",
        border_radius="8px"
    )
