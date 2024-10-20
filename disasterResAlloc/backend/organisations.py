import reflex as rx
from typing import Optional
from table_state import Organisation

org_1 = Organisation(name="Red Cross Gaza", location="Gaza", email="redcrossgaza@gmail.com", encoded_wallet="0x1234567890")
org_2 = Organisation(name="Amnesty International Gaza", location="Gaza", email="amnestygaza@gmail.com", encoded_wallet="0x1234567890")

with rx.session() as session:
    session.add(org_1)
    session.add(org_2)
    session.commit()

