from fastapi import status


class DomainException(Exception):
    def __init__(self, message: str, status_code: int = 500, code: str = 'GENERIC_ERROR') -> None:
        self.message = message
        self.status_code = status_code
        self.code = code
        super().__init__(message)


class ResourceNotFoundError(DomainException):
    def __init__(self, resource: str, **kwargs: dict) -> None:
        super().__init__(
            message=f'the resource {resource} was not found, try again.',
            code='RESOURCE_NOT_FOUND',
            status_code=status.HTTP_404_NOT_FOUND
        )
        self.kwargs = kwargs


class ResourceAlreadyExistsError(DomainException):
    def __init__(self, resource: str, **kwargs: dict) -> None:
        super().__init__(
            message=f'this resource {resource} already exists, try again.',
            code='RESOURCE_ALREADY_EXISTS',
            status_code=status.HTTP_409_CONFLICT
        )
        self.kwargs = kwargs


class InternalServerError(DomainException):
    def __init__(self, message: str, **kwargs: dict) -> None:
        super().__init__(message=message)
        self.kwargs = kwargs
