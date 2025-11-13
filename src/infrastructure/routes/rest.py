from fastapi.routing import APIRouter
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

import uuid

from domain import get_settings, EventInput, EventUpdateInput, TicketInput
import container


settings = get_settings()
prefix = f'/{settings.NAMESPACE}/api/{settings.API_VERSION}/{settings.RESOURCE}'
descriptions = {
    'liveness': 'Verify that the service is available.',
    'create_event': 'Create a new event.',
    'get_event': 'Get details of an event.',
    'update_event': 'Update an event already exists.',
    'delete_event': 'Delete a specify event.',
    'seller_ticket': 'Process to seller ticket with event_id.',
    'exchange_ticket': 'Process to exchange ticket.'
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
    with container.SingletonContainer.scope() as app:
        use_case = app.use_cases.update_event()
        response = use_case.execute(str(id), event)
        return JSONResponse(jsonable_encoder(response, exclude={'status_code'}),
                            status_code=response.status_code)


@rest_router.delete('/events/{id}', tags=['Events'],
            summary=descriptions['delete_event'])
def delete_event(id: uuid.UUID) -> dict:
    with container.SingletonContainer.scope() as app:
        use_case = app.use_cases.delete_event()
        response = use_case.execute(str(id))
        return JSONResponse(jsonable_encoder(response, exclude={'status_code'}),
                            status_code=response.status_code)


@rest_router.post('/tickets', tags=['Tickets'],
            summary=descriptions['seller_ticket'])
def seller_ticket(ticket: TicketInput) -> dict:
    with container.SingletonContainer.scope() as app:
        use_case = app.use_cases.seller_ticket()
        response = use_case.execute(ticket)
        return JSONResponse(jsonable_encoder(response, exclude={'status_code'}),
                            status_code=response.status_code)
    

@rest_router.patch('/tickets/{code}', tags=['Tickets'],
            summary=descriptions['exchange_ticket'])
def exchange_ticket(code: int) -> dict:
    with container.SingletonContainer.scope() as app:
        use_case = app.use_cases.exchange_ticket()
        response = use_case.execute(str(code))
        return JSONResponse(jsonable_encoder(response, exclude={'status_code'}),
                            status_code=response.status_code)

