class RepositoryException(Exception):
    def __init__(self, entity_type: str, operation: str, detail: str = ""):
        self.entity_type = entity_type
        self.operation = operation
        self.detail = detail
        message = f"Error in {entity_type} repository during {operation} operation"
        if detail:
            message += f": {detail}"
        super().__init__(message)


class RepositoryOperationException(RepositoryException):
    def __init__(self, entity_type: str, operation: str, detail: str):
        super().__init__(entity_type, operation, detail)
