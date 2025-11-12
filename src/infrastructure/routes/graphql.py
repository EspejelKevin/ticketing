import strawberry
from strawberry.fastapi import GraphQLRouter

import uuid

from domain import (get_settings,
                    EventInputType,
                    EventUpdateInputType,
                    EventDetailsType,
                    DomainErrorExtension)
import container


@strawberry.type
class Query:
    @strawberry.field
    def event_details(self, id: uuid.UUID) -> EventDetailsType:
        pass
    

@strawberry.type
class Mutation:
    @strawberry.mutation
    def create_event(self, event: EventInputType) -> str:
        with container.SingletonContainer.scope() as app:
            use_case = app.use_cases.create_event()
            data = use_case.execute(event)
            return ''

    @strawberry.mutation
    def update_event(self, id: uuid.UUID, event: EventUpdateInputType) -> EventDetailsType:
        pass
    
    @strawberry.mutation
    def delete_event(self, id: uuid.UUID) -> str:
        return 'event deleted'


settings = get_settings()
prefix = f'/{settings.NAMESPACE}/api/{settings.API_VERSION}/{settings.RESOURCE}/graphql'

schema = strawberry.Schema(query=Query, mutation=Mutation, extensions=[DomainErrorExtension])
graphql_router = GraphQLRouter(schema, prefix=prefix)
