from fastapi import status

import uuid
from datetime import datetime

from domain import (DBRepository, ResourceNotFoundError, ResourceConflictError,
                    Response, InternalServerError, TicketUpdateInput)
from log import Log


class ExchangeTicket:
    def __init__(self, db_service: DBRepository, log: Log) -> None:
        self.db_service = db_service
        self.log = log
        self.transaction_id = str(uuid.uuid4())
        self.timestamp = datetime.now()
        self.meta = {'transaction_id': self.transaction_id, 'timestamp': self.timestamp}
    
    def execute(self, code: str, ticket: TicketUpdateInput):
        ticket_db = self.db_service.get_ticket_by_code(code)
        exchange_value = ticket.exchange

        if not ticket_db:
            raise ResourceNotFoundError(resource=code, meta=self.meta)
        
        event_id = ticket_db[5]
        event_db = self.db_service.get_event_by_id(event_id)

        if not event_db:
            raise ResourceNotFoundError(resource=event_id, meta=self.meta)

        exchange_value_db = ticket_db[3]

        if exchange_value_db:
            message = f'ticket {code} status: it already was exchanged'
            raise ResourceConflictError(message=message, meta=self.meta)
        
        current_date = datetime.now()
        start_date = event_db[1]
        end_date = event_db[2]

        if current_date.date() < start_date.date() or current_date.date() > end_date.date():
            message = 'an error ocurred while changing the ticket status, because the current_date out of range'
            raise ResourceConflictError(message=message, meta=self.meta)

        ticket = {
            'exchange': exchange_value,
            'exchange_date': current_date
        }

        total_tickets_exchange = event_db[5]
        total_tickets_exchange += 1

        if not self.db_service.update_ticket(code, ticket):
            message = f'error while updating ticket: {code}'
            raise InternalServerError(message=message, meta=self.meta)
        
        if not self.db_service.update_event_tickets_exchanged(event_id, total_tickets_exchange):
            message = f'error while updating tickets exchanged of event: {event_id}'
            raise InternalServerError(message=message, meta=self.meta)

        return Response(data=ticket, meta=self.meta, status_code=status.HTTP_201_CREATED)
