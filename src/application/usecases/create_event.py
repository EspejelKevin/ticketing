from fastapi.exceptions import HTTPException

import uuid

from domain import DBRepository, EventInput
from log import Log


class CreateEvent:
    def __init__(self, db_service: DBRepository, log: Log) -> None:
        self.db_service = db_service
        self.log = log
    
    def execute(self, event: EventInput):
        event_db = self.db_service.get_event_by_name(event.name)

        if event_db:
            raise HTTPException(status_code=409, detail='event already exists')
        
        _id = str(uuid.uuid4())
        result = self.db_service.create_event(_id, event)

        if not result:
            return 'error while creating event, try again'
        
        return 'event created with success'
    


