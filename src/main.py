from fastapi import FastAPI
import uvicorn

from infrastructure import rest_router, graphql_router
import container


tags = [
    {
        'name': 'Health Checks',
        'description': 'Endpoints to check service availability.'
    },
    {
        'name': 'Events',
        'description': 'Endpoints to manage events'
    }
]

def on_start_up() -> None:
    container.SingletonContainer.init()

app = FastAPI(
    title='Ticketing System',
    openapi_tags=tags,
    on_startup=[on_start_up]
)
app.include_router(rest_router)
app.include_router(graphql_router, include_in_schema=False)


if __name__ == '__main__':
    uvicorn.run('main:app', host='0.0.0.0',
                port=8000, reload=False)
