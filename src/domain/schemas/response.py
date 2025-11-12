from pydantic import BaseModel
import strawberry

from datetime import datetime


class Response(BaseModel):
    data: dict
    meta: dict
    status_code: int


class EventDetails(BaseModel):
    name: str
    start_date: datetime
    end_date: datetime
    total_tickets_sold: int
    total_tickets_available: int
    total_tickets_exchange: int


@strawberry.experimental.pydantic.type(model=EventDetails, all_fields=True)
class EventDetailsType:
    pass
