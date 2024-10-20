"""Welcome to Reflex!."""

# Import all the pages.
from .pages import *
from .pages import organisation
from . import styles
from disasterResAlloc.backend.table_state import Organisation
import reflex as rx


# Create the app. 
app = rx.App(
    style=styles.base_style,
    stylesheets=styles.base_stylesheets,
    title="Disaster Relief Payment Gateway",
    description="A dashboard for fast payments for disaster relief.",
)
