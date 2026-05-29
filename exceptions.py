class APIRequestError(Exception):
    """Сбой при выполнении запроса к API Практикум Домашка."""


class APIStatusCodeError(Exception):
    """API вернул код ответа, отличный от 200."""
