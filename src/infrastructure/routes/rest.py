from fastapi.routing import APIRouter
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

import uuid

from domain import get_settings, EventInput, EventUpdateInput
import container


settings = get_settings()
prefix = f'/{settings.NAMESPACE}/api/{settings.API_VERSION}/{settings.RESOURCE}'
descriptions = {
    'liveness': 'Verify that the service is available.',
    'create_event': 'Create a new event.',
    'get_event': 'Get details of an event.',
    'update_event': 'Update an event already exists.',
    'delete_event': 'Delete a specify event.'
}

rest_router = APIRouter(prefix=prefix)


@rest_router.get('/liveness', tags=['Health Checks'],
            summary=descriptions['liveness'])
def liveness() -> dict:
    return {'status': 'success'}


@rest_router.post('/events', tags=['Events'],
            summary=descriptions['create_event'])
def create_event(event: EventInput) -> dict:
    with container.SingletonContainer.scope() as app:
        use_case = app.use_cases.create_event()
        response = use_case.execute(event)
        return JSONResponse(jsonable_encoder(response, exclude={'status_code'}),
                            status_code=response.status_code)


@rest_router.get('/events/{id}', tags=['Events'],
            summary=descriptions['get_event'])
def get_event_by_id(id: uuid.UUID) -> dict:
    with container.SingletonContainer.scope() as app:
        use_case = app.use_cases.event_details()
        response = use_case.execute(str(id))
        return JSONResponse(jsonable_encoder(response, exclude={'status_code'}),
                            status_code=response.status_code)


@rest_router.patch('/events/{id}', tags=['Events'],
            summary=descriptions['update_event'])
def update_event(id: uuid.UUID, event: EventUpdateInput) -> dict:
    return {'status': 'success', 'event': event.model_dump()}


@rest_router.delete('/events/{id}', tags=['Events'],
            summary=descriptions['delete_event'])
def delete_event(id: uuid.UUID) -> dict:
    return {'id': str(id)}
