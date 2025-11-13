import strawberry
from strawberry.fastapi import GraphQLRouter
from strawberry.scalars import JSON
from fastapi import status

import uuid

from domain import (get_settings, EventInputType, Response, ErrorResponse,
                    TicketInput, EventUpdateInputType, LivenessType, DomainException)
import container


@strawberry.type
class Query:
    error_response = ErrorResponse()

    @strawberry.field
    def liveness(self) -> LivenessType:
        return LivenessType()
    
    @strawberry.field
    def event_details(self, id: uuid.UUID) -> JSON:
        try:
            with container.SingletonContainer.scope() as app:
                use_case = app.use_cases.event_details()
                response: Response = use_case.execute(str(id))
                return response.model_dump(mode='json')
        except DomainException as ex:
            return Response(data=ex.data, meta=ex.meta, status_code=ex.status_code).model_dump(mode='json')
        except Exception as ex:
            return Query.error_response.dumps(str(ex), 'GENERIC_ERROR')
    

@strawberry.type
class Mutation:
    error_response = ErrorResponse()

    @strawberry.mutation
    def create_event(self, event: EventInputType) -> JSON:
        try:
            event = event.to_pydantic()
            with container.SingletonContainer.scope() as app:
                use_case = app.use_cases.create_event()
                response = use_case.execute(event)
                return response.model_dump(mode='json')
        except DomainException as ex:
            return Response(data=ex.data, meta=ex.meta, status_code=ex.status_code).model_dump(mode='json')
        except ValueError as ex:
            return Mutation.error_response.dumps(str(ex), 'BAD_REQUEST', status.HTTP_400_BAD_REQUEST)
        except Exception as ex:
            return Mutation.error_response.dumps(str(ex), 'GENERIC_ERROR')

    @strawberry.mutation
    def update_event(self, id: uuid.UUID, event: EventUpdateInputType) -> JSON:
        try:
            event = event.to_pydantic()
            with container.SingletonContainer.scope() as app:
                use_case = app.use_cases.update_event()
                response = use_case.execute(str(id), event)
                return response.model_dump(mode='json')
        except DomainException as ex:
            return Response(data=ex.data, meta=ex.meta, status_code=ex.status_code).model_dump(mode='json')
        except ValueError as ex:
            return Mutation.error_response.dumps(str(ex), 'BAD_REQUEST', status.HTTP_400_BAD_REQUEST)
        except Exception as ex:
            return Mutation.error_response.dumps(str(ex), 'GENERIC_ERROR')
    
    @strawberry.mutation
    def delete_event(self, id: uuid.UUID) -> JSON:
        try:
            with container.SingletonContainer.scope() as app:
                use_case = app.use_cases.delete_event()
                response = use_case.execute(str(id))
                return response.model_dump(mode='json')
        except DomainException as ex:
            return Response(data=ex.data, meta=ex.meta, status_code=ex.status_code).model_dump(mode='json')
        except Exception as ex:
            return Mutation.error_response.dumps(str(ex), 'GENERIC_ERROR')
        
    @strawberry.mutation
    def seller_ticket(self, event_id: uuid.UUID) -> JSON:
        try:
            with container.SingletonContainer.scope() as app:
                use_case = app.use_cases.seller_ticket()
                response = use_case.execute(TicketInput(event_id=event_id))
                return response.model_dump(mode='json')
        except DomainException as ex:
            return Response(data=ex.data, meta=ex.meta, status_code=ex.status_code).model_dump(mode='json')
        except Exception as ex:
            return Mutation.error_response.dumps(str(ex), 'GENERIC_ERROR')
        
    @strawberry.mutation
    def exchange_ticket(self, code: str) -> JSON:
        try:
            with container.SingletonContainer.scope() as app:
                use_case = app.use_cases.exchange_ticket()
                response = use_case.execute(code)
                return response.model_dump(mode='json')
        except DomainException as ex:
            return Response(data=ex.data, meta=ex.meta, status_code=ex.status_code).model_dump(mode='json')
        except Exception as ex:
            return Mutation.error_response.dumps(str(ex), 'GENERIC_ERROR')


settings = get_settings()
prefix = f'/{settings.NAMESPACE}/api/{settings.API_VERSION}/{settings.RESOURCE}/graphql'

schema = strawberry.Schema(query=Query, mutation=Mutation)
graphql_router = GraphQLRouter(schema, prefix=prefix)
