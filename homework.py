import logging
import os
import sys
import time
from http import HTTPStatus

import requests
import telebot
from dotenv import load_dotenv

import messages
from exceptions import APIRequestError, APIStatusCodeError

load_dotenv()


PRACTICUM_TOKEN = os.getenv('PRACTICUM_TOKEN')
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

RETRY_PERIOD = 600
ENDPOINT = 'https://practicum.yandex.ru/api/user_api/homework_statuses/'
HEADERS = {'Authorization': f'OAuth {PRACTICUM_TOKEN}'}


HOMEWORK_VERDICTS = {
    'approved': 'Работа проверена: ревьюеру всё понравилось. Ура!',
    'reviewing': 'Работа взята на проверку ревьюером.',
    'rejected': 'Работа проверена: у ревьюера есть замечания.'
}

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(
    logging.Formatter('%(asctime)s [%(levelname)s] %(message)s')
)
logger.addHandler(handler)


def check_tokens():
    """Смотрим, что все токены на месте."""
    tokens = {
        'PRACTICUM_TOKEN': PRACTICUM_TOKEN,
        'TELEGRAM_TOKEN': TELEGRAM_TOKEN,
        'TELEGRAM_CHAT_ID': TELEGRAM_CHAT_ID,
    }
    missing = [name for name, value in tokens.items() if not value]
    if missing:
        logger.critical(messages.MISSING_TOKENS.format(tokens=missing))
        return False
    return True


def send_message(bot, message):
    """Шлём сообщение в чат."""
    try:
        bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message)
    except (telebot.apihelper.ApiException,
            requests.RequestException) as error:
        logger.error(messages.SEND_MESSAGE_ERROR.format(error=error))
    else:
        logger.debug(messages.MESSAGE_SENT.format(message=message))


def get_api_answer(timestamp):
    """Дёргаем апи и отдаём ответ словарём."""
    try:
        response = requests.get(
            ENDPOINT,
            headers=HEADERS,
            params={'from_date': timestamp},
        )
    except requests.RequestException as error:
        raise APIRequestError(
            messages.API_REQUEST_ERROR.format(
                endpoint=ENDPOINT, error=error
            )
        )
    if response.status_code != HTTPStatus.OK:
        raise APIStatusCodeError(
            messages.API_STATUS_ERROR.format(
                endpoint=ENDPOINT, code=response.status_code
            )
        )
    return response.json()


def check_response(response):
    """Проверяем, что ответ апи не кривой."""
    if not isinstance(response, dict):
        raise TypeError(messages.RESPONSE_NOT_DICT)
    if 'homeworks' not in response:
        raise KeyError(messages.NO_HOMEWORKS_KEY)
    homeworks = response['homeworks']
    if not isinstance(homeworks, list):
        raise TypeError(messages.HOMEWORKS_NOT_LIST)
    return homeworks


def parse_status(homework):
    """Достаём статус домашки и собираем текст."""
    if 'homework_name' not in homework:
        raise KeyError(messages.NO_HOMEWORK_NAME_KEY)
    homework_name = homework['homework_name']
    status = homework.get('status')
    if status not in HOMEWORK_VERDICTS:
        raise ValueError(messages.UNKNOWN_STATUS.format(status=status))
    verdict = HOMEWORK_VERDICTS[status]
    return messages.STATUS_CHANGED.format(
        name=homework_name, verdict=verdict
    )


def main():
    """Тут вся логика бота крутится."""
    if not check_tokens():
        sys.exit(messages.NO_TOKENS_EXIT)

    bot = telebot.TeleBot(token=TELEGRAM_TOKEN)
    timestamp = int(time.time())
    last_message = ''

    while True:
        try:
            response = get_api_answer(timestamp)
            homeworks = check_response(response)
            if homeworks:
                message = parse_status(homeworks[0])
            else:
                message = ''
                logger.debug(messages.NO_NEW_STATUSES)
            if message and message != last_message:
                send_message(bot, message)
                last_message = message
            timestamp = response.get('current_date', timestamp)
        except Exception as error:
            message = messages.PROGRAM_FAILURE.format(error=error)
            logger.error(message)
            if message != last_message:
                send_message(bot, message)
                last_message = message
        finally:
            time.sleep(RETRY_PERIOD)


if __name__ == '__main__':
    main()
