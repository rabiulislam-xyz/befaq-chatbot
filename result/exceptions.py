class MessageProcessingError(Exception):
    pass


class InvalidMessageError(MessageProcessingError):
    pass


class ResultNotFoundError(MessageProcessingError):
    pass

