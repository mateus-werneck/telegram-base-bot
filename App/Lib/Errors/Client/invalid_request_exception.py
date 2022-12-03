class InvalidRequestException(Exception):
    def __init__(self, api: str):
        message = f'Invalid request when trying to call {api}'
        super().__init__(message)
