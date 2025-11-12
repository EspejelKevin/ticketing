from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from .errors import (ResourceNotFoundError,
                     ResourceAlreadyExistsError, 
                     InternalServerError)


def resource_not_found_handler(_, ex: ResourceNotFoundError) -> JSONResponse:
    return core_handler(ex)


def resource_already_exists_handler(_, ex: ResourceAlreadyExistsError) -> JSONResponse:
    return core_handler(ex)


def internal_server_handler(_, ex: InternalServerError) -> JSONResponse:
    return core_handler(ex)


def core_handler(ex: Exception) -> JSONResponse:
    content = {'data': {'message': ex.message, 'code': ex.code}}
    if ex.kwargs:
        content.update(ex.kwargs)
    return JSONResponse(content=jsonable_encoder(content), status_code=ex.status_code)
