from datetime import datetime
import reflex as rx
from typing import Optional, Union, List
from sqlalchemy import select, String 
import csv


class Item(rx.Base):
    """The item class."""

    name: str
    payment: float
    date: str
    status: str


class Organisation(rx.Model, table=True):
    """NGO class"""
    name: str
    location: str
    email: str
    encoded_wallet: str
    created: datetime = datetime.now()
    updated: Optional[datetime] = None
    seed: Optional[str] = None


class TableState(rx.State):
    """The state class."""
    items: List[Item] = []

    search_value: str = ""
    sort_value: str = ""
    sort_reverse: bool = False

    total_items: int = 0
    offset: int = 0
    limit: int = 12  # Number of rows per page

    @rx.var(cache=True)
    def filtered_sorted_items(self) -> List[Item]:
        items = self.items

        # Filter items based on selected item
        if self.sort_value:
            if self.sort_value in ["payment"]:
                items = sorted(
                    items,
                    key=lambda item: float(getattr(item, self.sort_value)),
                    reverse=self.sort_reverse,
                )
            else:
                items = sorted(
                    items,
                    key=lambda item: str(getattr(item, self.sort_value)).lower(),
                    reverse=self.sort_reverse,
                )

        # Filter items based on search value
        if self.search_value:
            search_value = self.search_value.lower()
            items = [
                item
                for item in items
                if any(
                    search_value in str(getattr(item, attr)).lower()
                    for attr in [
                        "name",
                        "payment",
                        "date",
                        "status",
                    ]
                )
            ]

        return items

    @rx.var(cache=True)
    def page_number(self) -> int:
        return (self.offset // self.limit) + 1

    @rx.var(cache=True)
    def total_pages(self) -> int:
        return (self.total_items // self.limit) + (
            1 if self.total_items % self.limit else 0
        )

    @rx.var(cache=True, initial_value=[])
    def get_current_page(self) -> list[Item]:
        start_index = self.offset
        end_index = start_index + self.limit
        return self.filtered_sorted_items[start_index:end_index]

    def prev_page(self):
        if self.page_number > 1:
            self.offset -= self.limit

    def next_page(self):
        if self.page_number < self.total_pages:
            self.offset += self.limit

    def first_page(self):
        self.offset = 0

    def last_page(self):
        self.offset = (self.total_pages - 1) * self.limit

    def load_entries(self):
        with open("items.csv", mode="r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            self.items = [Item(**row) for row in reader]
            self.total_items = len(self.items)

    def toggle_sort(self):
        self.sort_reverse = not self.sort_reverse
        self.load_entries()

    # Organisation search logic 
    search_query: str = ""
    search_results: List[Organisation] = []

    def set_search_query(self, query: str):
        self.search_query = query 
        self.search_organisation()

    def search_organisation(self):
        # """Search organisation table based on search query"""
        with rx.session() as session:
            search_value = f"%{self.search_query}%"
            results = session.execute(
                select(Organisation).filter(Organisation.name.ilike(search_value))
            ).scalars().all()
            self.search_results = results

    async def get_organisation_by_id(self, org_id: str):
        """Fetch an organisation by its ID."""
        try:
            async with rx.session() as session:
                organisation = await session.exec(
                    select(Organisation).filter(Organisation.id == org_id)
                ).scalar_one_or_none()
                self.organisation = organisation  # Store result in state
        except Exception as e:
            self.error_message = f"Error: {str(e)}"

    async def on_load(self):
        """Fetch the organisation when the page loads."""
        await self.get_organisation_by_id(rx.State.id)