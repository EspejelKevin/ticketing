from fastapi import status

import uuid
from datetime import datetime

from domain import (DBRepository, ResourceNotFoundError, ResourceConflictError,
                    BadRequestError, Response, InternalServerError, EventUpdateInput)
from log import Log


class UpdateEvent:
    def __init__(self, db_service: DBRepository, log: Log) -> None:
        self.db_service = db_service
        self.log = log
        self.transaction_id = str(uuid.uuid4())
        self.timestamp = datetime.now()
        self.meta = {'transaction_id': self.transaction_id, 'timestamp': self.timestamp}
    
    def execute(self, _id: str, event: EventUpdateInput):
        self.log.info('start logic update_event')

        event_db = self.db_service.get_event_by_id(_id)

        if not event_db:
            self.log.info('resource not found in database', extra={'details': {'event_id': _id}})
            raise ResourceNotFoundError(resource=_id, meta=self.meta)
        
        event_db = list(event_db)
        start_date_from_db = event_db[1]
        new_end_date = event.end_date

        if new_end_date and new_end_date.date() < start_date_from_db.date():
            self.log.info('conflict between new_end_date and start_date_from_db',
                          extra={'details': {'new_end_date': new_end_date, 'start_date_from_db': start_date_from_db}})
            message = 'new end_date can not be less than start_date initial'
            raise BadRequestError(message=message, meta=self.meta)

        total_tickets_from_db = event_db[3]
        total_tickets_sold_from_db = event_db[4]
        new_total_tickets = event.total_tickets
        
        if new_total_tickets:
            if new_total_tickets < total_tickets_sold_from_db:
                self.log.info('conflict between new_total_tickets and total_tickets_sold_from_db',
                          extra={'details': {'new_total_tickets': new_total_tickets, 'total_tickets_sold_from_db': total_tickets_sold_from_db}})
                message = 'total_tickets can not be less than total_tickets_sold'
                details = f'max quantity allowed to decrease is: {total_tickets_from_db - total_tickets_sold_from_db}'
                raise BadRequestError(message=message, meta=self.meta, details=details)
            
            event_db[3] = new_total_tickets
        
        current_date = datetime.now()
        end_date_from_db = event_db[2]
        
        if current_date.date() > end_date_from_db.date():
            event_name = event_db[0]
            message = f'the event {event_name} can not be updated becasue has finished'
            raise ResourceConflictError(message=message, meta=self.meta)
        
        event.name = event_db[0] if not event.name else event.name
        event.start_date = event_db[1] if not event.start_date else event.start_date
        event.end_date = event_db[2] if not event.end_date else event.end_date
        event.total_tickets = event_db[3]

        if self.db_service.update_event(_id, event) is None:
            message = f'error while updating event {_id}'
            raise InternalServerError(message=message, meta=self.meta)

        data = {
            'name': event.name,
            'start_date': event.start_date,
            'end_date': event.end_date,
            'total_tickets_available': event.total_tickets - total_tickets_sold_from_db,
            'total_tickets_sold': total_tickets_sold_from_db,
            'total_tickets_exchange': event_db[5]
        }

        self.log.info('update event with success')

        return Response(data=data, meta=self.meta, status_code=status.HTTP_200_OK)