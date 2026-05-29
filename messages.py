"""Тексты сообщений, логов и ошибок бота.

Я подумал, что логичнее хранить их отдельно,
чтобы при правке текста не лезть в основной код (допустим на будущее).
"""

# Логи
MISSING_TOKENS = 'Отсутствуют переменные окружения: {tokens}'
MESSAGE_SENT = 'Бот отправил сообщение "{message}"'
SEND_MESSAGE_ERROR = 'Не удалось отправить сообщение в Telegram: {error}'
NO_NEW_STATUSES = 'Новых статусов в ответе нет.'
PROGRAM_FAILURE = 'Сбой в работе программы: {error}'

# Ошибки запроса к API
API_REQUEST_ERROR = 'Сбой при запросе к эндпоинту {endpoint}: {error}'
API_STATUS_ERROR = ('Эндпоинт {endpoint} недоступен. '
                    'Код ответа API: {code}')

# Ошибки проверки ответа
RESPONSE_NOT_DICT = 'Ответ API должен быть словарём.'
NO_HOMEWORKS_KEY = 'В ответе API нет ключа "homeworks".'
HOMEWORKS_NOT_LIST = 'Домашки в ответе API должны быть списком.'
NO_HOMEWORK_NAME_KEY = 'В ответе API нет ключа "homework_name".'
UNKNOWN_STATUS = 'Неизвестный статус работы: "{status}".'

# Сообщение пользователю
STATUS_CHANGED = 'Изменился статус проверки работы "{name}". {verdict}'

# Завершение программы
NO_TOKENS_EXIT = 'Программа остановлена: нет переменных окружения.'
