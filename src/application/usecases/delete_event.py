from fastapi import status

import uuid
from datetime import datetime

from domain import DBRepository, ResourceNotFoundError, Response, InternalServerError
from log import Log


class DeleteEvent:
    def __init__(self, db_service: DBRepository, log: Log) -> None:
        self.db_service = db_service
        self.log = log
        self.transaction_id = str(uuid.uuid4())
        self.timestamp = datetime.now()
        self.meta = {'transaction_id': self.transaction_id, 'timestamp': self.timestamp}
    
    def execute(self, _id: str):
        self.log.info('start logic delete_event')

        data = {
            'event_id': _id,
            'message': 'the event can not be delete because is active or has tickets sold'
        }

        event_db = self.db_service.get_event_by_id(_id)

        if not event_db:
            self.log.info('resource not found in database', extra={'details': {'event_id': _id}})
            raise ResourceNotFoundError(resource=_id, meta=self.meta)
        
        current_date = datetime.now()
        end_date = event_db[2]
        total_tickets_sold = event_db[4]

        if (current_date > end_date) or total_tickets_sold == 0:
            if not self.db_service.delete_event_by_id(_id):
                message = f'error while deleting event {_id}'
                raise InternalServerError(message=message, meta=self.meta)

            data = {
                'name': event_db[0],
                'start_date': event_db[1],
                'end_date': event_db[2],
                'total_tickets_available': event_db[3] - event_db[4],
                'total_tickets_sold': event_db[4],
                'total_tickets_exchange': event_db[5]
            }

        self.log.info('event deleted with success')
        
        return Response(data=data, meta=self.meta, status_code=status.HTTP_200_OK)
