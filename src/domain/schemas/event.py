from pydantic import BaseModel, Field, model_validator
import strawberry

from typing import Self
from datetime import datetime


# SCHEMAS FOR REST API

class EventInput(BaseModel):
    name: str = Field(min_length=5, max_length=50)
    start_date: datetime
    end_date: datetime
    total_tickets: int = Field(ge=1, le=300)

    @model_validator(mode='after')
    def validate_dates(self) -> Self:
        if self.start_date.date() <= datetime.now().date():
            raise ValueError('start_date must be greater than now date')
        
        if self.end_date.date() < self.start_date.date():
            raise ValueError('end_date must be greater than start_date')
        return self


class EventUpdateInput(BaseModel):
    name: str | None = Field(default=None, min_length=5, max_length=50)
    start_date: datetime | None = None
    end_date: datetime | None = None
    total_tickets: int | None = Field(default=None, ge=1, le=300)

    @model_validator(mode='after')
    def validate_dates(self) -> Self:
        if self.start_date and self.start_date.date() <= datetime.now().date():
            raise ValueError('start_date must be greater than now date')

        if (self.end_date and self.start_date) and (self.end_date.date() < self.start_date.date()):
            raise ValueError('end_date must be greater than start_date')
        return self
    

class EventDetails(BaseModel):
    name: str
    start_date: datetime
    end_date: datetime
    total_tickets_sold: int
    total_tickets_available: int
    total_tickets_exchange: int


# SCHEMAS FOR GRAPHQL

@strawberry.experimental.pydantic.input(model=EventInput, all_fields=True)
class EventInputType:
    pass


@strawberry.experimental.pydantic.input(model=EventUpdateInput, all_fields=True)
class EventUpdateInputType:
    pass


@strawberry.experimental.pydantic.type(model=EventDetails, all_fields=True)
class EventDetailsType:
    pass
