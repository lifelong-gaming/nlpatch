class BaseError(Exception):
    def __init__(self, message: str):
        super(BaseError, self).__init__(message)
