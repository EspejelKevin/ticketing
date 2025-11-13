from fastapi import status

import uuid
from datetime import datetime

from domain import (DBRepository, EventInput, 
                    ResourceAlreadyExistsError,
                    InternalServerError, Response)
from log import Log


class CreateEvent:
    def __init__(self, db_service: DBRepository, log: Log) -> None:
        self.db_service = db_service
        self.log = log
        self.transaction_id = str(uuid.uuid4())
        self.timestamp = datetime.now()
        self.meta = {'transaction_id': self.transaction_id, 'timestamp': self.timestamp}
    
    def execute(self, event: EventInput):
        self.log.info('start logic create_event')

        event_db = self.db_service.get_event_by_name(event.name)

        if event_db:
            self.log.info('resource already exists in database', extra={'details': {'event': event.name}})
            raise ResourceAlreadyExistsError(resource=event.name, meta=self.meta)
        
        _id = str(uuid.uuid4())
        result = self.db_service.create_event(_id, event)

        if not result:
            message = f'error while creating event {event.name}'
            raise InternalServerError(message=message, meta=self.meta)
        
        data = {
            'id': _id,
            'name': event.name,
            'start_date': event.start_date,
            'end_date': event.end_date
        }

        self.log.info('event created with success')

        return Response(data=data, meta=self.meta, status_code=status.HTTP_201_CREATED)
