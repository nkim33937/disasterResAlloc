import reflex as rx
from ..templates import template
from ..backend.table_state import TableState

@template(route=f"/organisation/[id]", title="Organisation Details")
def organisation() -> rx.Component:
    organisation = TableState.get_organisation_by_id('abc')

    return rx.vstack(
        rx.heading(f"Organisation: {organisation.name}", size="3"),
        rx.text(f"Location: {organisation.location}"),
        rx.text(f"Email: {organisation.email}"),
        rx.text(f"Encoded Wallet: {organisation.encoded_wallet}"),
        rx.text(f"Created: {organisation.created}"),
        rx.text(f"Last Updated: {organisation.updated}"),
        rx.button("Donate", color_scheme="blue"),
        spacing="8",
        width="100%",
    )