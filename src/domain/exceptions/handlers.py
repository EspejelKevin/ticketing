from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from .errors import (ResourceNotFoundError, ResourceAlreadyExistsError, DomainException,
                     InternalServerError, BadRequestError, ResourceConflictError)


def bad_request_handler(_, ex: BadRequestError) -> JSONResponse:
    return core_handler(ex)


def resource_conflict_handler(_, ex: ResourceConflictError) -> JSONResponse:
    return core_handler(ex)


def resource_not_found_handler(_, ex: ResourceNotFoundError) -> JSONResponse:
    return core_handler(ex)


def resource_already_exists_handler(_, ex: ResourceAlreadyExistsError) -> JSONResponse:
    return core_handler(ex)


def internal_server_handler(_, ex: InternalServerError) -> JSONResponse:
    return core_handler(ex)


def core_handler(ex: DomainException) -> JSONResponse:
    content = {'data': ex.data, 'meta': ex.meta}
    return JSONResponse(content=jsonable_encoder(content), status_code=ex.status_code)
