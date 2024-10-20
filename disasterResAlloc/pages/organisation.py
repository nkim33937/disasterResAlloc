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


@rx.page(route="/organisation/[id]", title="Organisation Details")
def organisation() -> rx.Component:
    # Conditionally render content based on the organisation state

    return rx.container(
        rx.text('Organisation Details', style={"font-size": "24px", "font-weight": "bold", 'text_align': "center", 'padding': '20px'}),
        rx.text('Name: ', Organisations.selected_org['name']),  # Display the wallet address from state
        rx.text('Location: ', Organisations.selected_org['location']),  # Display the wallet address from state
        rx.container(
            # rx.button('Donate', on_click=rx.set_value(Organisations.donate_modal, True)),  # Display the wallet address from state
            rx.button('Back', on_click=rx.redirect("/")),
            padding="20px",
            border="1px solid #ddd",
            border_radius="0px",
            style={"margin-top": "20px", "display": "flex", "justify-content": "center"}
        ),

        on_mount=Organisations.get_Organisations(),
        padding="20px",
        # border="1px solid #ddd",
        border_radius="8px"
    )