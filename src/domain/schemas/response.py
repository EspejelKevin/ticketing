from pydantic import BaseModel
import strawberry

from typing import Dict
import uuid
from datetime import datetime


class Response(BaseModel):
    data: Dict
    meta: Dict
    status_code: int


class ErrorResponse(BaseModel):
    data: Dict | None = None
    meta: Dict | None = None
    status_code: int | None = None

    def dumps(self, message: str, code: str, status_code: int = 500, details: str = '') -> dict:
        self.data = {'message': message, 'code': code, 'details': details}
        self.meta = {'transaction_id': str(uuid.uuid4()), 'timestamp': datetime.now()}
        self.status_code = status_code
        return self.model_dump(mode='json')


@strawberry.type
class LivenessType:
    status: str = 'success'
