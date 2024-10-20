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
    return rx.vstack(
        rx.heading(f"Welcome, Red Cross International", size="5"),
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
                style=[styles.ghost_button_style],
            )),
        ),
        card(
            rx.hstack(
                tab_content_header(),
                rx.segmented_control.root(
                    rx.segmented_control.item("Donation Total", value="revenue"),
                    margin_bottom="1.5em",
                    default_value="users",
                    on_change=StatsState.set_selected_tab,
                ),
                width="100%",
                justify="between",
            ),
            rx.match(
                StatsState.selected_tab,
                ("revenue", revenue_chart()),
            ),
        ),
        spacing="8",
        width="100%",
    )
