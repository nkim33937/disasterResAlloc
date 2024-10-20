import reflex as rx
import sqlalchemy

from disasterResAlloc import styles
from ..templates import template
from ..backend.routes import get_Organisation
from ..backend.table_state import *
from ..components.wallet import create_multiple_wallets, send_xrp

class Organisations(rx.State):
    # ... (rest of your Organisations class)

@rx.page(route="/organisation/[id]", title="Organisation Details")
def organisation() -> rx.Component:
    return rx.container(
        # Background Image
        rx.image(
            f"{Organisations.selected_org['image']}",
            style={
                "width": "2048px",
                "height": "60%",
                "overflow": "fit",
                "object-fit": "cover",
                "position": "absolute",
                "top": "0",
                "left": "0",
                "z-index": "-1",
            },
        ),
        rx.container(
            # Organisation Name
            rx.text(
                f"{Organisations.selected_org['name']}",
                style={
                    "padding": "10px",
                    "text-align": "center",
                    "font-size": "20px",
                    "font-weight": "bold",
                    "margin-top": "75%",
                },
            ),
            # Disaster Info
            rx.text(
                f"{Organisations.selected_org['disaster']}",
                style={"padding": "10px", "text-align": "center"},
            ),
            # Location with Icon
            rx.flex(
                rx.icon("map-pin", size=20),
                rx.text(
                    f"{Organisations.selected_org['location']}",
                    style={"padding": "10px", "text-align": "center"},
                ),
                align="center",
                gap="2",
                justify="center",
            ),
            # Cause
            rx.text(
                f"{Organisations.selected_org['cause']}",
                style={"padding": "10px", "text-align": "center"},
            ),
            # NGO Balance
            rx.text(
                f"NGO Balance: {Organisations.NGO['balance']} XRP",
                style={"padding": "10px", "text-align": "center"},
            ),
            # Donate Button and Modal
            rx.container(
                rx.dialog.root(
                    rx.center(
                        rx.dialog.trigger(
                            rx.button(
                                rx.text("Donate", size="4"),
                                justify="center",
                            ),
                            justify="center",
                            style={
                                "display": "flex",
                                "justify-content": "center",
                            },
                        ),
                    ),
                    rx.dialog.content(
                        rx.dialog.title(
                            f"Donate XRP: Current Balance: {Organisations.NGO['balance']} XRP"
                        ),
                        rx.dialog.description(
                            "How much would you like to donate?",
                            style={"padding-bottom": "10px"},
                        ),
                        rx.form(
                            rx.flex(
                                # Amount Input
                                rx.input(
                                    placeholder="$0",
                                    name="Amount",
                                    padding="10px",
                                ),
                                # Cancel and Submit Buttons
                                rx.flex(
                                    rx.dialog.close(
                                        rx.button(
                                            "Cancel",
                                            variant="soft",
                                            color_scheme="gray",
                                        ),
                                    ),
                                    rx.dialog.close(
                                        rx.button(
                                            "Submit", type="submit"
                                        ),
                                    ),
                                    spacing="3",
                                    justify="end",
                                ),
                                direction="column",
                                spacing="4",
                            ),
                            on_submit=Organisations.donate,
                            reset_on_submit=False,
                        ),
                        max_width="450px",
                    ),
                ),
                padding="20px",
                border_radius="0px",
                justify="space-between",
                style={
                    "margin-top": "20px",
                    "justify-content": "space-between",
                    "align-items": "center",
                },
            ),
            on_mount=Organisations.get_Organisations(),
            padding="20px",
            border_radius="8px",
        ),
        # Back Arrow Icon
        rx.icon(
            "arrow-left",
            size=50,
            on_click=rx.redirect("/"),
            style={
                "left": "30px",
                "top": "30px",
                "position": "absolute",
                "padding": "10px",
                "border-radius": "12px",
                "background-color": "rgba(255, 255, 255, 0.3)",
                "color": styles.text_color,
                "cursor": "pointer",
                ":hover": {
                    "color": styles.accent_text_color,
                    "background-color": styles.gray_bg_color,
                },
            },
        ),
    )
