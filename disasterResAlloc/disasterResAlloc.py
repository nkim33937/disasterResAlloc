"""Welcome to Reflex!."""

# Import all the pages.
from .pages import *
from .pages import organisation
from . import styles
from disasterResAlloc.backend.table_state import Organisation
from .pages.wallet import WalletPage
import reflex as rx

# from pages import *
# import styles
# from pages.wallet import WalletPage



# Create the app. 
app = rx.App(
    style=styles.base_style,
    stylesheets=styles.base_stylesheets,
    title="Disaster Relief Payment Gateway",
    description="A dashboard for fast payments for disaster relief.",
)

# # Add the pages
# app.add_page(WalletPage, route="/wallet")

print("Adding WalletPage...")
app.add_page(WalletPage, route="/wallet")
print("WalletPage added.")

# Compile the app
app._compile()