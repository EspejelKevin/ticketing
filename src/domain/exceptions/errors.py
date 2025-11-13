from fastapi import status


class DomainException(Exception):
    def __init__(self, message: str, meta: dict, status_code: int = 500, code: str = 'GENERIC_ERROR', **kwargs) -> None:
        self.data = {'message': message, 'code': code, 'details': kwargs.get('details', '')}
        self.meta = meta
        self.status_code = status_code
        super().__init__(message)


class BadRequestError(DomainException):
    def __init__(self, message: str, meta: dict, **kwargs: dict) -> None:
        super().__init__(message=message, meta=meta,
            code='BAD_REQUEST_ERROR', status_code=status.HTTP_400_BAD_REQUEST, **kwargs)


class ResourceConflictError(DomainException):
    def __init__(self, message: str, meta: dict, **kwargs: dict) -> None:
        super().__init__(message=message, meta=meta,
            code='RESOURCE_CONFLICT', status_code=status.HTTP_409_CONFLICT, **kwargs)


class ResourceNotFoundError(DomainException):
    def __init__(self, resource: str, meta: dict, **kwargs: dict) -> None:
        super().__init__(message=f'the resource {resource} was not found, try again.', meta=meta,
            code='RESOURCE_NOT_FOUND', status_code=status.HTTP_404_NOT_FOUND, **kwargs)


class ResourceAlreadyExistsError(DomainException):
    def __init__(self, resource: str, meta: dict, **kwargs: dict) -> None:
        super().__init__(message=f'this resource {resource} already exists, try again.', meta=meta,
            code='RESOURCE_ALREADY_EXISTS', status_code=status.HTTP_409_CONFLICT, **kwargs)


class InternalServerError(DomainException):
    def __init__(self, message: str, meta: dict, **kwargs: dict) -> None:
        super().__init__(message=message, meta=meta, **kwargs)
