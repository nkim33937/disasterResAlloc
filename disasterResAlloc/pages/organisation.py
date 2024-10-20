import reflex as rx
import sqlalchemy

from disasterResAlloc import styles
from ..templates import template
from ..backend.routes import get_Organisation
from ..backend.table_state import *
from ..components.wallet import create_multiple_wallets, send_xrp

class Organisations(rx.State):
    orgs: list[Organisation] = []
    selected_org: Optional[Organisation] = None
    donate_modal: bool = False # Modal state
    NGO = {}
    async def initialize_wallet(self):
        
        try:
            # Create a single wallet
            wallets = await create_multiple_wallets(1)
            if wallets and len(wallets) > 0:
                new_wallet = wallets[0]
                
                # Fund the wallet with 10000 XRP
                amount = 10000
                result = await send_xrp(new_wallet['classicAddress'], amount)
                
                if result:
                    # Update the organisation's wallet and balance in the database
                    org_id = self.router.page.full_raw_path.split("/")[-2]
                    with rx.session() as session:
                        session.exec(
                            sqlalchemy.text("UPDATE organisation SET encoded_wallet = :wallet, balance = :balance WHERE id = :id")
                            .bindparams(wallet=new_wallet['classicAddress'], balance=amount, id=org_id)
                        )
                        session.commit()
                    
                    # Update the state
                    self.NGO['encoded_wallet'] = new_wallet['classicAddress']
                    self.NGO['balance'] = amount
                    
                    print(f"Wallet initialized with {amount} XRP: {new_wallet['classicAddress']}")
                else:
                    print("Failed to fund the wallet")
            else:
                print("Failed to create a wallet")
        except Exception as e:
            print(f"Error initializing wallet: {str(e)}")

    def get_Organisations(self):
        """Fetch all organisations from the database."""
        try:
            org_id = self.router.page.full_raw_path.split("/")[-2]
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
    
    def donate(self, form_data: dict):
        amount = float(form_data.get("Amount", 0))
        ngo_balance = self.NGO.get('balance', 10000)  # Use .get() with a default value

        if amount <= 0 or amount > ngo_balance:
            return

        recipient = self.selected_org['encoded_wallet'] if self.selected_org else ""
        result = send_xrp(self.NGO.get('encoded_wallet', ''), recipient, amount)


        if result:
            self.NGO['balance'] = self.NGO['balance'] - amount
            org_id = self.router.page.full_raw_path.split("/")[-2]
            with rx.session() as session:
                org = session.exec(sqlalchemy.select(Organisation).where(Organisation.id == org_id)).one()
                org.balance += amount
                session.commit()
            
            if self.selected_org:
                self.selected_org['balance'] += amount

        
        self.close_donate_modal()
        

        
        
        
        

        pass

    def fetch_balance(self):
        try:
            org_id = self.router.page.full_raw_path.split("/")[-2]
            with rx.session() as session:
                result = session.exec(
                    sqlalchemy.text("SELECT balance FROM organisation WHERE id = :id").bindparams(id=org_id),
                )
                ###either store in a class variable or return the value
                print(result.scalar_one())
                return result.scalar_one()
        except Exception as e:
            print(f"Error fetching balance: {str(e)}")

    def update_balance(self, amount: float):
        try:
            org_id = self.router.page.full_raw_path.split("/")[-2]
            with rx.session() as session:
                result = session.exec(
                    sqlalchemy.update("organisation").where("id" == org_id).values(balance=amount),
                )
                ###either store in a class variable or return the value
                print(result.scalar_one())
                return result.scalar_one()
        except Exception as e:
            print(f"Error fetching balance: {str(e)}")
@rx.page(route="/organisation/[id]", title="Organisation Details")
def organisation() -> rx.Component:
    # Conditionally render content based on the organisation state

    return rx.container(
                rx.image(f"{Organisations.selected_org['image']}", style={"width":"2048px", "height":"60%", "overflow":"fit", "object-fit":"cover", "position":"absolute", "top":"0", "left":"0", "z-index":"-1"}),
        rx.container(
        # rx.text('_____', style={"font-size": "24px", "font-weight": "bold", 'text_align': "center", 'padding': '20px', }),
        rx.text(f"{Organisations.selected_org['name']}", style={"padding": "10px", "text-align": "center", "font-size": "20px", "font-weight": "bold", "margin-top":"75%"}),  # Display the wallet address from state
        rx.text(f"{Organisations.selected_org['disaster']}", style={"padding": "10px", "text-align": "center"}),  # Display the wallet address from state
        rx.flex(rx.icon('map-pin', size=20),
        rx.text(f"{Organisations.selected_org['location']}", style={"padding": "10px", "text-align": "center"}),  # Display the wallet address from state
        align="center",
        gap="2",
        justify="center",
        ),
        rx.text(f"{Organisations.selected_org['cause']}", style={"padding": "10px", "text-align": "center"}),  # Display the wallet address from state
        rx.text(f"NGO Balance: {Organisations.NGO['balance']} XRP", style={"padding": "10px", "text-align": "center"}),
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
                        # "Donate XRP: Current Balance: {self.NGO['balance']}",
                        f"NGO Balance: {Organisations.NGO['balance']} XRP",
                    ),
                    rx.dialog.description(
                        "How much would you like to donate?",
                    style={"padding-bottom": "10px"}),
                    rx.form(
                        rx.flex(
                            rx.input(
                                placeholder="$0",
                                name="Amount",
                                padding="10px",
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
    rx.icon('arrow-left', size=50, on_click=rx.redirect("/"), style={"left": "30px", "top": "30px", "position": "absolute", "padding": "10px","border-radius": "12px", "background-color": "rgba(255, 255, 255, 0.3)", "color": styles.text_color, "cursor": "pointer", ":hover": {"color": styles.accent_text_color, "background-color": styles.gray_bg_color}}),            
    )