from fastapi import status

import uuid
from datetime import datetime

from domain import (DBRepository, ResourceNotFoundError, ResourceConflictError,
                    Response, InternalServerError)
from log import Log


class ExchangeTicket:
    def __init__(self, db_service: DBRepository, log: Log) -> None:
        self.db_service = db_service
        self.log = log
        self.transaction_id = str(uuid.uuid4())
        self.timestamp = datetime.now()
        self.meta = {'transaction_id': self.transaction_id, 'timestamp': self.timestamp}
    
    def execute(self, code: str):
        self.log.info('start logic exchange_ticket')

        ticket_db = self.db_service.get_ticket_by_code(code)

        if not ticket_db:
            self.log.info('resource not found in database', extra={'details': {'ticket_code': code}})
            raise ResourceNotFoundError(resource=code, meta=self.meta)
        
        event_id = ticket_db[5]
        event_db = self.db_service.get_event_by_id(event_id)

        if not event_db:
            self.log.info('resource not found in database', extra={'details': {'event_id': event_id}})
            raise ResourceNotFoundError(resource=event_id, meta=self.meta)

        exchange_value_db = ticket_db[3]
        exchange_date = ticket_db[4]

        if exchange_value_db:
            self.log.info('the ticket has been exchanged previously',
                          extra={'details': {'ticket_code': code, 'exchange_date': exchange_date}})
            message = f'ticket {code} status: it already was exchanged'
            raise ResourceConflictError(message=message, meta=self.meta)
        
        current_date = datetime.now()
        start_date = event_db[1]
        end_date = event_db[2]

        if current_date.date() < start_date.date() or current_date.date() > end_date.date():
            self.log.info('error with the dates, not match',
                          extra={'details': {'current_date': current_date, 'start_date': start_date, 'end_date': end_date}})
            message = 'an error ocurred while changing the ticket status, because the current_date out of range'
            raise ResourceConflictError(message=message, meta=self.meta)

        ticket = {
            'exchange': True,
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
        
        self.log.info('exchange ticket with success')

        return Response(data=ticket, meta=self.meta, status_code=status.HTTP_200_OK)
