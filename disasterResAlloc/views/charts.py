import reflex as rx
import random
import datetime
from typing import List, Dict, Any
from reflex.components.radix.themes.base import (
    LiteralAccentColor,
)


class StatsState(rx.State):
    area_toggle: bool = True
    selected_tab: str = "donation"
    timeframe: str = "Monthly"
    users_data: List[Dict[str, Any]] = []
    revenue_data: List[Dict[str, Any]] = []
    orders_data: List[Dict[str, Any]] = []
    device_data: List[Dict[str, Any]] = []
    yearly_device_data: List[Dict[str, Any]] = []
    donation_data: List[Dict[str, Any]] = []
    all_org_donation_data: Dict[str, List[Dict[str, Any]]] = {}

    def toggle_areachart(self):
        self.area_toggle = not self.area_toggle

    def randomize_data(self):
        from ..backend.table_state import TableState
        for org in TableState.organisations:
            self.all_org_donation_data[org.id] = generate_dummy_donation_data()
        # If data is already populated, don't randomize
        # if self.donation_data:
        #     return
        
        # self.donation_data = []
        # for i in range(30, -1, -1):  # Include today's data
        #     self.revenue_data.append(
        #         {
        #             "Date": (
        #                 datetime.datetime.now() - datetime.timedelta(days=i)
        #             ).strftime("%m-%d"),
        #             "Revenue": random.randint(1000, 5000),
        #         }
        #     )
        # print("Randomized donation data:", self.donation_data)
        # for i in range(30, -1, -1):
        #     self.orders_data.append(
        #         {
        #             "Date": (
        #                 datetime.datetime.now() - datetime.timedelta(days=i)
        #             ).strftime("%m-%d"),
        #             "Orders": random.randint(100, 500),
        #         }
        #     )

        # for i in range(30, -1, -1):
        #     self.users_data.append(
        #         {
        #             "Date": (
        #                 datetime.datetime.now() - datetime.timedelta(days=i)
        #             ).strftime("%m-%d"),
        #             "Users": random.randint(100, 500),
        #         }
        #     )

        # self.device_data = [
        #     {"name": "Desktop", "value": 23, "fill": "var(--blue-8)"},
        #     {"name": "Mobile", "value": 47, "fill": "var(--green-8)"},
        #     {"name": "Tablet", "value": 25, "fill": "var(--purple-8)"},
        #     {"name": "Other", "value": 5, "fill": "var(--red-8)"},
        # ]

        # self.yearly_device_data = [
        #     {"name": "Desktop", "value": 34, "fill": "var(--blue-8)"},
        #     {"name": "Mobile", "value": 46, "fill": "var(--green-8)"},
        #     {"name": "Tablet", "value": 21, "fill": "var(--purple-8)"},
        #     {"name": "Other", "value": 9, "fill": "var(--red-8)"},
        # ]

    def get_total_donations(self) -> List[Dict[str, Any]]:
        total_donations = {}
        for org_data in self.all_org_donation_data.values():
            for donation in org_data:
                date = donation["Date"]
                amount = donation["Donations"]
                #existing = next((item for item in total_donations if item["Date"] == date), None)
                if date in total_donations: 
                    total_donations[date] += amount
                else:
                    total_donations[date] = amount
        return [{"Date": date, "Donations": amount} for date, amount in sorted(total_donations.items())]

    def toggle_areachart(self):
        self.area_toggle = not self.area_toggle

    def set_selected_tab(self, tab: str):
        self.selected_tab = tab

    def set_timeframe(self, timeframe: str):
        self.timeframe = timeframe

def area_toggle() -> rx.Component:
    return rx.cond(
        StatsState.area_toggle,
        rx.icon_button(
            rx.icon("area-chart"),
            size="2",
            cursor="pointer",
            variant="surface",
            on_click=StatsState.toggle_areachart,
        ),
        rx.icon_button(
            rx.icon("bar-chart-3"),
            size="2",
            cursor="pointer",
            variant="surface",
            on_click=StatsState.toggle_areachart,
        ),
    )


def _create_gradient(color: LiteralAccentColor, id: str) -> rx.Component:
    return (
        rx.el.svg.defs(
            rx.el.svg.linear_gradient(
                rx.el.svg.stop(
                    stop_color=rx.color(color, 7), offset="5%", stop_opacity=0.8
                ),
                rx.el.svg.stop(stop_color=rx.color(color, 7), offset="95%", stop_opacity=0),
                x1=0,
                x2=0,
                y1=0,
                y2=1,
                id=id,
            ),
        ),
    )


def _custom_tooltip(color: LiteralAccentColor) -> rx.Component:
    return (
        rx.recharts.graphing_tooltip(
            separator=" : ",
            content_style={
                "backgroundColor": rx.color("gray", 1),
                "borderRadius": "var(--radius-2)",
                "borderWidth": "1px",
                "borderColor": rx.color(color, 7),
                "padding": "0.5rem",
                "boxShadow": "0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1)",
            },
            is_animation_active=True,
        ),
    )


def users_chart() -> rx.Component:
    return rx.cond(
        StatsState.area_toggle,
        rx.recharts.area_chart(
            _create_gradient("blue", "colorBlue"),
            _custom_tooltip("blue"),
            rx.recharts.cartesian_grid(
                stroke_dasharray="3 3",
            ),
            rx.recharts.area(
                data_key="Users",
                stroke=rx.color("blue", 9),
                fill="url(#colorBlue)",
                type_="monotone",
            ),
            rx.recharts.x_axis(data_key="Date", scale="auto"),
            rx.recharts.y_axis(),
            rx.recharts.legend(),
            data=StatsState.users_data,
            height=425,
        ),
        rx.recharts.bar_chart(
            rx.recharts.cartesian_grid(
                stroke_dasharray="3 3",
            ),
            _custom_tooltip("blue"),
            rx.recharts.bar(
                data_key="Users",
                stroke=rx.color("blue", 9),
                fill=rx.color("blue", 7),
            ),
            rx.recharts.x_axis(data_key="Date", scale="auto"),
            rx.recharts.y_axis(),
            rx.recharts.legend(),
            data=StatsState.users_data,
            height=425,
        ),
    )


def revenue_chart() -> rx.Component:
    return rx.cond(
        StatsState.area_toggle,
        rx.recharts.area_chart(
            _create_gradient("green", "colorGreen"),
            _custom_tooltip("green"),
            rx.recharts.cartesian_grid(
                stroke_dasharray="3 3",
            ),
            rx.recharts.area(
                data_key="Revenue",
                stroke=rx.color("green", 9),
                fill="url(#colorGreen)",
                type_="monotone",
            ),
            rx.recharts.x_axis(data_key="Date", scale="auto"),
            rx.recharts.y_axis(),
            rx.recharts.legend(),
            data=StatsState.revenue_data,
            height=425,
        ),
        rx.recharts.bar_chart(
            _custom_tooltip("green"),
            rx.recharts.cartesian_grid(
                stroke_dasharray="3 3",
            ),
            rx.recharts.bar(
                data_key="Revenue",
                stroke=rx.color("green", 9),
                fill=rx.color("green", 7),
            ),
            rx.recharts.x_axis(data_key="Date", scale="auto"),
            rx.recharts.y_axis(),
            rx.recharts.legend(),
            data=StatsState.revenue_data,
            height=425,
        ),
    )

def generate_dummy_donation_data(num_transactions=10) -> List[Dict[str, Any]]:
    donation_data = []
    for _ in range(num_transactions):
        date = (datetime.datetime.now() - datetime.timedelta(days=random.randint(0, 30))).strftime("%m-%d")
        amount = random.randint(10, 1000)
        donation_data.append({"Date": date, "Donations": amount})
    return sorted(donation_data, key=lambda x: x["Date"])

def donation_history_chart(donation_data_func) -> rx.Component:
    @rx.var
    def get_data():
        if callable(donation_data_func):
            return donation_data_func()
        return donation_data_func
    
    chart_data = rx.Var.create(get_data)

    return rx.cond(
        StatsState.area_toggle,
        rx.recharts.area_chart(
            _create_gradient("green", "colorGreen"),
            _custom_tooltip("green"),
            rx.recharts.cartesian_grid(stroke_dasharray="3 3"),
            rx.recharts.area(
                data_key="Donations",
                stroke=rx.color("green", 9),
                fill="url(#colorGreen)",
                type_="monotone",
            ),
            rx.recharts.x_axis(data_key="Date", scale="auto"),
            rx.recharts.y_axis(),
            rx.recharts.legend(),
            data=chart_data,
            height=425,
            width="100%",
        ),
        rx.recharts.bar_chart(
            _custom_tooltip("green"),
            rx.recharts.cartesian_grid(stroke_dasharray="3 3"),
            rx.recharts.bar(
                data_key="Donations",
                stroke=rx.color("green", 9),
                fill=rx.color("green", 7),
            ),
            rx.recharts.x_axis(data_key="Date", scale="auto"),
            rx.recharts.y_axis(),
            rx.recharts.legend(),
            data=chart_data,
            height=425,
            width="100%",
        ),
    )

def orders_chart() -> rx.Component:
    return rx.cond(
        StatsState.area_toggle,
        rx.recharts.area_chart(
            _create_gradient("purple", "colorPurple"),
            _custom_tooltip("purple"),
            rx.recharts.cartesian_grid(
                stroke_dasharray="3 3",
            ),
            rx.recharts.area(
                data_key="Orders",
                stroke=rx.color("purple", 9),
                fill="url(#colorPurple)",
                type_="monotone",
            ),
            rx.recharts.x_axis(data_key="Date", scale="auto"),
            rx.recharts.y_axis(),
            rx.recharts.legend(),
            data=StatsState.orders_data,
            height=425,
        ),
        rx.recharts.bar_chart(
            _custom_tooltip("purple"),
            rx.recharts.cartesian_grid(
                stroke_dasharray="3 3",
            ),
            rx.recharts.bar(
                data_key="Orders",
                stroke=rx.color("purple", 9),
                fill=rx.color("purple", 7),
            ),
            rx.recharts.x_axis(data_key="Date", scale="auto"),
            rx.recharts.y_axis(),
            rx.recharts.legend(),
            data=StatsState.orders_data,
            height=425,
        ),
    )


def pie_chart() -> rx.Component:
    return rx.cond(
        StatsState.timeframe == "Yearly",
        rx.recharts.pie_chart(
            rx.recharts.pie(
                data=StatsState.yearly_device_data,
                data_key="value",
                name_key="name",
                cx="50%",
                cy="50%",
                padding_angle=1,
                inner_radius="70",
                outer_radius="100",
                label=True,
            ),
            rx.recharts.legend(),
            height=300,
        ),
        rx.recharts.pie_chart(
            rx.recharts.pie(
                data=StatsState.device_data,
                data_key="value",
                name_key="name",
                cx="50%",
                cy="50%",
                padding_angle=1,
                inner_radius="70",
                outer_radius="100",
                label=True,
            ),
            rx.recharts.legend(),
            height=300,
        ),
    )


def timeframe_select() -> rx.Component:
    return rx.select(
        ["Monthly", "Yearly"],
        default_value="Monthly",
        value=StatsState.timeframe,
        variant="surface",
        on_change=StatsState.set_timeframe,
    )

# def charts() -> rx.Component:
#     return rx.box(
#         rx.tabs(
#             rx.tab_list(
#                 rx.tab("Donations", value="donations"),
#                 rx.tab("Users", value="users"),
#                 rx.tab("Revenue", value="revenue"),
#                 rx.tab("Orders", value="orders"),
#             ),
#             rx.tab_panels(
#                 rx.tab_panel(donation_history_chart(), value="donations"),
#                 rx.tab_panel(users_chart(), value="users"),
#                 rx.tab_panel(revenue_chart(), value="revenue"),
#                 rx.tab_panel(orders_chart(), value="orders"),
#             ),
#             value=StatsState.selected_tab,
#             on_value_change=StatsState.set_selected_tab,
#         ),
#         rx.hstack(
#             area_toggle(),
#             timeframe_select(),
#             justify="end",
#         ),
#     )