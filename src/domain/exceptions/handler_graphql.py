from strawberry.extensions import SchemaExtension
from graphql import GraphQLError

from .errors import (ResourceNotFoundError,
                     ResourceAlreadyExistsError,
                     InternalServerError)


class DomainErrorExtension(SchemaExtension):
    def on_operation(self):
        yield

        execution_result = self.execution_context.result

        if execution_result and getattr(execution_result, 'errors', None):
            execution_result.errors = [self._format_error(error) for error in execution_result.errors]
    
    def _format_error(self, error: GraphQLError) -> GraphQLError:
        original_error = error.original_error
        classes = (ResourceNotFoundError,
                   ResourceAlreadyExistsError,
                   InternalServerError)

        if isinstance(original_error, classes):
            new_extensions = {
                'code': original_error.code,
                'status_code': original_error.status_code
            }
        
            if error.extensions:
                error.extensions.update(new_extensions)
            else:
                error.extensions = new_extensions

            return error
        
        return GraphQLError(
            message='Unexpected error occurred.',
            nodes=error.nodes,
            source=error.source,
            positions=error.positions,
            path=error.path,
            original_error=InternalServerError('an error ocurred while executing internal process.')
        )
