class APIStatusCodeError(Exception):
    """API вернул код ответа, отличный от 200."""


class TokensError(Exception):
    """Не хватает обязательных переменных окружения."""
