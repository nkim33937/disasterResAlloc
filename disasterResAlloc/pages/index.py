"""The overview page of the app."""

import reflex as rx
from .. import styles
from ..templates import template
from ..views.stats_cards import stats_cards
from ..views.charts import (
    users_chart,
    revenue_chart,
    orders_chart,
    area_toggle,
    pie_chart,
    timeframe_select,
    StatsState,
    donation_history_chart,
)
from ..views.adquisition_view import adquisition
from ..components.notification import notification
from ..components.card import card
from ..backend.table_state import TableState
# from .profile import ProfileState
import datetime


def _time_data() -> rx.Component:
    return rx.hstack(
        rx.tooltip(
            rx.icon("info", size=20),
            content=f"{(datetime.datetime.now() - datetime.timedelta(days=30)).strftime('%b %d, %Y')} - {datetime.datetime.now().strftime('%b %d, %Y')}",
        ),
        rx.text("Last 30 days", size="4", weight="medium"),
        align="center",
        spacing="2",
        display=["none", "none", "flex"],
    )

def special_events_example():
    return rx.button(
        "Alert", on_click=rx.window_alert("Hello World!")
    )

def tab_content_header() -> rx.Component:
    return rx.hstack(
        _time_data(),
        area_toggle(),
        align="center",
        width="100%",
        spacing="4",
    )


@template(route="/", title="Overview", on_load=StatsState.randomize_data)
def index() -> rx.Component:
    """The overview page.

    Returns:
        The UI for the overview page.
    """
    # donation_data = [
    #     {"Date": "10-01", "Donation": 100},
    #     {"Date": "10-05", "Donation": 500},
    #     {"Date": "10-10", "Donation": 800},
    #     {"Date": "10-15", "Donation": 200},
    #     {"Date": "10-20", "Donation": 400},
    #     {"Date": "10-25", "Donation": 300},
    # ]

    return rx.vstack(
        rx.heading(f"Welcome, Organization", size="5", style={ 
                "width": "20%",    
                "animation": "typing 1.5s steps(40, end), blink-caret .75s step-end infinite",
                "animation-fill-mode": "forwards",
                "white-space": "nowrap",
                "overflow": "hidden",
                "@keyframes typing": {
                    "from": { "width": "0" },
                    "to": { "width": "23%" }
                },
                # "@keyframes blink-caret": {
                #     "from": { "border-right": ".15em solid grey" },
                #     "50%": { "border-right": "transparent" },
                #     "to": { "border-right": "none" }

                # }
                }),
        stats_cards(),
        rx.flex(
            rx.input(
                rx.input.slot(rx.icon("search"), padding_left="0"),
                placeholder="Search Relief Organisations...",
                size="3",
                width="100%",
                max_width="450px",
                radius="large",
                style=styles.ghost_input_style,
                on_change=rx.event(TableState.set_search_query),
            ),
            justify="between",
            align="center",
            width="100%",
        ),
        rx.cond(
            TableState.search_query != "",
            rx.foreach(TableState.search_results, lambda org: rx.button(
                rx.box(
                    rx.text(f"{org.name}", color=styles.text_color, hover_color=styles.accent_text_color, style={"padding":"20px", "border-radius":"12px",":hover": {"background_color": styles.gray_bg_color}}),
                    # rx.text(f"Location: {org.location}"),
                    # rx.text(f"Email: {org.email}")
                    # rx.text(f"Wallet: {org.encoded_wallet}"),
                ),
                on_click=rx.redirect(f"/organisation/{org.id}"),
                style=[styles.ghost_button_style, {
                "animation": "slide-down 0.5s ease-out",
                "@keyframes slide-down": {
                    "from": {"transform": "translateY(-20px)", "opacity": "0"},
                    "to": {"transform": "translateY(0)", "opacity": "1"},
                },
            }],
            )),
        ),
        card(
            rx.hstack(
                tab_content_header(),
                rx.segmented_control.root(
                    rx.segmented_control.item("Donation Total", value="donation"),
                    margin_bottom="1.5em",
                    default_value="donation",
                    on_change=StatsState.set_selected_tab,
                ),
                width="100%",
                justify="between",
            ),
            rx.cond(
                StatsState.selected_tab == "donation",
                donation_history_chart(),
                #("donation", donation_history_chart()),
                #("revenue", revenue_chart()),
                rx.text("Select 'Donation Total' to view the chart"),
            ),
        ),
        spacing="8",
        width="100%",
    )
