"""Welcome to Reflex!."""

# Import all the pages.
from .pages import *
from . import styles
from .pages.wallet import WalletPage
import reflex as rx

# Create the app.
app = rx.App(
    style=styles.base_style,
    stylesheets=styles.base_stylesheets,
    title="Dashboard Template",
    description="A dashboard template for Reflex.",
)

# Add the pages
app.add_page(WalletPage, route="/wallet")

# Compile the app
app.compile()