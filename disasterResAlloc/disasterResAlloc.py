"""Welcome to Reflex!."""

# Import all the pages.
from .pages import *
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

org_1 = Organisation(name="Red Cross Gaza", location="Gaza", email="redcrossgaza@gmail.com", encoded_wallet="0x1234567890")
org_2 = Organisation(name="Amnesty International Gaza", location="Gaza", email="amnestygaza@gmail.com", encoded_wallet="0x1234567890")

with rx.session() as session:
    session.add(org_1)
    session.add(org_2)
    session.commit()
    session.refresh(org_1)
    session.refresh(org_2)
