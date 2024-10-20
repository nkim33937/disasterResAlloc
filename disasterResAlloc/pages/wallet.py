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

# import reflex as rx
# from ..states.walletState import WalletState  # Import the state

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
import reflex as rx
from ..states.walletState import WalletState



# def WalletPage() -> rx.Component:
#     return rx.container(
#         rx.vstack(
#             rx.heading("XRPL Wallet Generator and Transfer"),
#             rx.input(
#                 placeholder="Number of wallets",
#                 type="number",
#                 min=1,
#                 max=10,
#                 value=WalletState.num_wallets,
#                 on_change=WalletState.set_num_wallets,
#             ),
#             rx.button(
#                 "Generate Wallets",
#                 on_click=WalletState.generate_wallets
#             ),
#             rx.button(
#                 "Clear Wallets",
#                 on_click=WalletState.clear_wallets
#             ),
#             rx.text(WalletState.status_message),
#             rx.ordered_list(
#                 rx.foreach(
#                     WalletState.wallet_addresses,
#                     lambda address, index: rx.list_item(f"Wallet {index}: {address}")
#                 )
#             ),
#             rx.hstack(
#                 rx.input(placeholder="Sender Wallet Index", type="number", id="sender_index"),
#                 rx.input(placeholder="Receiver Wallet Index", type="number", id="receiver_index"),
#                 rx.input(placeholder="Amount XRP", type="number", step="0.000001", id="amount"),
#                 # rx.button(
#                 #     "Send XRP",
#                 #     on_click=lambda: WalletState.send_xrp_between_wallets(
#                 #         # int(rx.State.get("sender_index")),
#                 #         # int(rx.State.get("receiver_index")),
#                 #         # rx.State.get("amount")
                        
#                 #         sender_index=int(rx.State.get("sender_index")),
#                 #         receiver_index=int(rx.State.get("receiver_index")),
#                 #         amount=float(rx.State.get("amount"))
#                 #     )
#                 # )
#                 rx.button(
#                     "Send XRP",
#                     # on_click=lambda: WalletState.send_xrp_between_wallets(
#                     #     sender_index=rx.Var.create("sender_index"),
#                     #     receiver_index=rx.Var.create("receiver_index"),
#                     #     amount=rx.Var.create("amount")
#                     # )
#                     on_click=lambda: WalletState.send_xrp_between_wallets(
#                         rx.Var.create("sender_index"),
#                         rx.Var.create("receiver_index"),
#                         rx.Var.create("amount")
#                         # sender_index=rx.Var.create("sender_index"),
#                         # receiver_index=rx.Var.create("receiver_index"),
#                         # amount=rx.Var.create("amount")
#                     )
#                 )
#             ),
#             spacing="4",
#             align_items="start",
#         ),
#         max_width="800px",
#         margin="0 auto",
#         padding="20px",
#         border="1px solid #ddd",
#         border_radius="8px"
#     )

# # def WalletPage():
# #     return rx.box(
# #         rx.heading("Wallet Page"),
# #         rx.text("This is a simple wallet page for testing.")
# #     )


def WalletPage() -> rx.Component:
    return rx.container(
        rx.vstack(
            rx.heading("XRPL Wallet Generator and Transfer"),
            rx.input(
                placeholder="Number of wallets",
                type="number",
                min=1,
                max=10,
                value=WalletState.num_wallets,
                on_change=WalletState.set_num_wallets,
            ),
            rx.hstack(
                rx.button(
                    "Generate Wallets",
                    on_click=WalletState.generate_wallets,  # Event handler
                    color_scheme="green",
                ),
                rx.button(
                    "Clear Wallets",
                    on_click=WalletState.clear_wallets,
                    color_scheme="red",
                ),
                spacing="4",
            ),
            rx.text(WalletState.status_message),
            rx.divider(),
            rx.heading("Wallet Addresses", size="md"),
            rx.ordered_list(
                rx.foreach(
                    WalletState.wallet_addresses,
                    lambda address, index: rx.list_item(f"Wallet {index}: {address}")
                )
            ),
            rx.divider(),
            rx.heading("Send XRP Between Wallets", size="md"),
            rx.hstack(
                rx.input(
                    placeholder="Sender Wallet Index",
                    type="number",
                    min=0,
                    value=WalletState.sender_index,
                    on_change=WalletState.set_sender_index,
                    width="100%",
                ),
                rx.input(
                    placeholder="Receiver Wallet Index",
                    type="number",
                    min=0,
                    value=WalletState.receiver_index,
                    on_change=WalletState.set_receiver_index,
                    width="100%",
                ),
                rx.input(
                    placeholder="Amount XRP",
                    type="number",
                    step="0.000001",
                    min=0.0,
                    value=WalletState.amount,
                    on_change=WalletState.set_amount,
                    width="100%",
                ),
                spacing="4",
            ),
            rx.button(
                "Send XRP",
                on_click=WalletState.send_xrp_between_wallets,
                color_scheme="blue",
                width="100%",
            ),
            spacing="4",
            align_items="start",
        ),
        max_width="800px",
        margin="0 auto",
        padding="20px",
        border="1px solid #ddd",
        border_radius="8px",
    )

