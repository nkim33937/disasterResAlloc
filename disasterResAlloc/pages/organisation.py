import reflex as rx
import sqlalchemy
from ..templates import template
from ..backend.routes import get_Organisation
from ..backend.table_state import *

class Organisations(rx.State):
    orgs: list[Organisation] = []
    selected_org: Optional[Organisation] = None
    donate_modal: bool = False # Modal state
    def current_url(self) -> str:
        print('URL', self.router.page.full_raw_path)
        url = self.router.page.full_raw_path.split("/")
        print('URL', url)
        return 

    def get_Organisations(self):
        """Fetch all organisations from the database."""
        try:
            org_id = self.router.page.full_raw_path.split("/")[-2]
            print('hi my', org_id)
            with rx.session() as session:
                result = session.exec(
                    sqlalchemy.text("SELECT * FROM organisation WHERE id = :id").bindparams(id=org_id),
                )
                # Store the result as a list of dictionaries in the state
                self.orgs = [dict(row) for row in result.mappings().all()]
                self.selected_org = self.orgs[0] if self.orgs else None
        except Exception as e:
            print(f"Error fetching organisations: {str(e)}")
    donate_modal: bool = False  # State to control modal visibility

    def open_donate_modal(self):
        """Open the donate modal by setting the state to True."""
        self.donate_modal = True

    def close_donate_modal(self):
        """Close the donate modal by setting the state to False."""
        self.donate_modal = False
    
    def donate(self, amount: float):
        pass
@rx.page(route="/organisation/[id]", title="Organisation Details")
def organisation() -> rx.Component:
    # Conditionally render content based on the organisation state

    return rx.container(rx.container(
        rx.text('Organisation Details', style={"font-size": "24px", "font-weight": "bold", 'text_align': "center", 'padding': '20px'}),
        rx.text(f"{Organisations.selected_org['name']}", style={"padding": "10px", "text-align": "center"}),  # Display the wallet address from state
        rx.text(f"Location: {Organisations.selected_org['location']}", style={"padding": "10px", "text-align": "center"}),  # Display the wallet address from state
        rx.container(
        rx.dialog.root(
            rx.center(
                rx.dialog.trigger(
                    rx.button(
                        rx.text("Donate", size="4"), justify="center", 
                    ),
                    justify="center",
                    style={"display": "flex", "justify-content": "center"}  # Center the button
                ),),
                rx.dialog.content(
                    rx.dialog.title(
                        "Donate XRP!",
                    ),
                    rx.dialog.description(
                        "How much would you like to donate?",
                    style={"padding": "10px"}),
                    rx.form(
                        rx.flex(
                            rx.input(
                                placeholder="$0",
                                name="Amount",
                            ),
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
            # border="1px solid #ddd",
            border_radius="0px",
            justify="space-between",
            style={"margin-top": "20px", "justify-content": "space-between", "align-items": "center"}
        ),
        on_mount=Organisations.get_Organisations(),
        padding="20px",
        # border="1px solid #ddd",
        border_radius="8px",
    ),        
    rx.button('Back', on_click=rx.redirect("/"), style={"font-size": "18px", "right": "30px", "bottom": "30px", "position": "absolute", "padding": "10px", "border-radius": "5px", "background-color": "red", "color": "white"}),            
    )