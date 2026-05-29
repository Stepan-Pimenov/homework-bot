"""Тексты сообщений, логов и ошибок бота."""

# Логи
MISSING_TOKENS = 'Отсутствуют переменные окружения: {tokens}'
MESSAGE_SENT = 'Бот отправил сообщение "{message}"'
SEND_MESSAGE_ERROR = 'Не удалось отправить сообщение в Telegram: {error}'
NO_NEW_STATUSES = 'Новых статусов в ответе нет.'
PROGRAM_FAILURE = 'Сбой в работе программы: {error}'
API_REQUEST_START = (
    'Делаем запрос к {url} с заголовками {headers} '
    'и параметрами {params}.'
)

# Ошибки запроса к API
API_REQUEST_ERROR = (
    'Сбой при запросе к {url} с заголовками {headers} '
    'и параметрами {params}: {error}'
)
API_STATUS_ERROR = (
    'Эндпоинт недоступен. Код ответа: {code}, '
    'причина: {reason}, текст: {text}.'
)

# Ошибки проверки ответа
RESPONSE_NOT_DICT = 'Ответ API должен быть словарём.'
NO_HOMEWORKS_KEY = 'В ответе API нет ключа "homeworks".'
HOMEWORKS_NOT_LIST = 'Домашки в ответе API должны быть списком.'
NO_HOMEWORK_NAME_KEY = 'В ответе API нет ключа "homework_name".'
UNEXPECTED_STATUS = 'Неожиданный статус работы: "{status}".'

# Сообщение пользователю
STATUS_CHANGED = 'Изменился статус проверки работы "{name}". {verdict}'
