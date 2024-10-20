import reflex as rx
from typing import Optional

"""API methods to handle Organisations."""
import json
from datetime import datetime, timezone

from fastapi import APIRouter, Request
from fastapi.exceptions import HTTPException

import reflex as rx

from .table_state import Organisation


async def get_Organisation(spec_id: int):
    """Get the Organisation associated with spec_id."""
    with rx.session() as session:
        spec = session.exec(Organisation).get(spec_id)
    return spec if spec else HTTPException(status_code=404)


async def list_Organisation(req: Request):
    """Get a list of all the Organisations."""
    with rx.session() as session:
        specs = session.exec(Organisation).all()
    return specs


async def add_Organisation(req: Request):
    """Add a new Organisation."""
    data = json.loads(await req.body())
    with rx.session() as session:
        now = datetime.now(timezone.utc)
        code = data["code"]
        if not code:
            return HTTPException(status_code=402, detail="Invalid `code`")
        session.add(
            Organisation(
                name=data["name"],
                location=data["location"],
                email=data["email"],
                encoded_wallet=data["encoded_wallet"],
                created=now,
            )
        )
        session.commit()
    return "OK"


async def update_Organisation(spec_id: int, req: Request):
    """Update the Organisation associated with spec_id."""
    data = json.loads(await req.body())
    with rx.session() as session:
        spec = session.exec(Organisation).get(spec_id)
        for k, v in data.items():
            setattr(spec, k, v)
            spec.updated = datetime.now(timezone.utc)
            spec.__setattr__(k, v)
            spec.__setattr__("updated", datetime.now())
        session.add(spec)
        session.commit()


async def delete_Organisation(spec_id):
    """Delete the Organisation associated with spec_id."""
    with rx.session() as session:
        spec = session.exec(Organisation).get(spec_id)
        session.delete(spec)
        session.commit()


Organisation_router = APIRouter(prefix="/Organisations", tags=["Organisations"])

Organisation_router.add_api_route("", add_Organisation, methods=["POST"])
Organisation_router.add_api_route("", list_Organisation, methods=["GET"])
Organisation_router.add_api_route("/{spec_id}", get_Organisation, methods=["GET"])
Organisation_router.add_api_route("/{spec_id}", update_Organisation, methods=["PUT"])
Organisation_router.add_api_route("/{spec_id}", delete_Organisation, methods=["DELETE"])