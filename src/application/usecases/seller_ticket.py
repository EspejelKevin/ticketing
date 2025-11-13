from fastapi import status

import uuid
from datetime import datetime

from domain import (DBRepository, ResourceNotFoundError, ResourceConflictError,
                    Response, InternalServerError, TicketInput)
from log import Log


class SellerTicket:
    def __init__(self, db_service: DBRepository, log: Log) -> None:
        self.db_service = db_service
        self.log = log
        self.transaction_id = str(uuid.uuid4())
        self.timestamp = datetime.now()
        self.meta = {'transaction_id': self.transaction_id, 'timestamp': self.timestamp}
    
    def execute(self, ticket: TicketInput):
        self.log.info('start logic seller_ticket')

        event_id = str(ticket.event_id)
        event_db = self.db_service.get_event_by_id(event_id)

        if not event_db:
            self.log.info('resource not found in database', extra={'details': {'event_id': event_id}})
            raise ResourceNotFoundError(resource=event_id, meta=self.meta)
        
        total_tickets = event_db[3]
        total_tickets_sold = event_db[4]
        event_name = event_db[0]

        if total_tickets_sold >= total_tickets:
            self.log.info('conflict between total_tickets and tickets_sold',
                          extra={'details': {'quantity_total_tickets': total_tickets, 'tickets_sold': total_tickets_sold}})
            message = f'event {event_name} status: there are not available tickets'
            raise ResourceConflictError(message=message, meta=self.meta)
        
        ticket = {
            'id': str(uuid.uuid4()),
            'code': str(uuid.uuid4().int),
            'sale_date': datetime.now(),
            'event_id': event_id
        }

        total_tickets_sold += 1

        if not self.db_service.create_ticket(ticket):
            message = f'error while creating ticket for event: {event_name}'
            raise InternalServerError(message=message, meta=self.meta)
        
        if not self.db_service.update_event_tickets_sold(event_id, total_tickets_sold):
            message = f'error while updating tickets sold of event: {event_name}'
            raise InternalServerError(message=message, meta=self.meta)
        
        self.log.info('seller ticket with success')

        return Response(data=ticket, meta=self.meta, status_code=status.HTTP_201_CREATED)
        