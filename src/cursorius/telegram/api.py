import logging
from typing import Literal, TypeAlias
import aiohttp
import requests


logger = logging.getLogger("cursorius")
log_handler = logging.StreamHandler()
log_handler.setFormatter(
    logging.Formatter(
        "{asctime} | {name} | {levelname} | {message}", style="{")
)
logger.addHandler(log_handler)

PARSE_MODE: TypeAlias = Literal["HTML", "MarkdownV2"]


class TelegramCursorius:
    """
    Delivery a message to a recipient using Telegram.

    :param str template: example: '<b>[{INSTANCE}] [ {APP_NAME} ]></b><br> {MESSAGE}\n {EXC_TYPE} | {EXC_VALUE}'
    :param str parse_mode: 'HTML' or 'MarkdownV2'
    :param str token: Telegram bot token
    :param str chat_id: Telegram chat id
    """

    def __init__(self, template: str, parse_mode: PARSE_MODE, token: str, chat_id: str):
        self._template = self._validate_template(template)
        self._parse_mode = parse_mode
        self._token = token
        self._chat_id = chat_id

    def send(self, **kwargs):
        try:
            url = self._get_url(**kwargs)
            self._execute_request(url)
        except:
            return

    async def send_async(self, **kwargs):
        try:
            url = self._get_url(**kwargs)
            await self._execute_request_async(url)
        except:
            return

    def _validate_template(self, template: str) -> str:
        _template = template.replace('\n', '%0A')
        valid_template = _template.replace('<br>', '%0A')

        # TODO: Implement additional validation logic here

        return valid_template

    def _get_url(self, **kwargs) -> str:
        message = self._get_format_message(**kwargs)
        url = self._fill_url(message)

        return url

    def _get_format_message(self, **kwargs) -> str:
        try:
            result = self._template.format(**kwargs)
        except KeyError as e:
            logger.warning('KeyError: ' + str(e), exc_info=True)
            raise e
        except Exception as e:
            logger.warning('Unexpected error: ' + str(e), exc_info=True)
            raise e

        return result

    def _fill_url(self, text: str):
        url = "https://api.telegram.org/bot" + self._token \
            + "/sendMessage?chat_id=" + self._chat_id \
            + "&text=" + text \
            + "&parse_mode=" + self._parse_mode

        return url

    def _execute_request(self, url):
        try:
            response = requests.get(url)
            response.raise_for_status()
        except requests.HTTPError as e:
            logger.warning('HTTPError: ' + str(e), exc_info=True)
            raise e
        except Exception as e:
            logger.warning('Unexpected error: ' + str(e), exc_info=True)
            raise e

    async def _execute_request_async(self, url):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    response.raise_for_status()
        except aiohttp.ClientResponseError as e:
            logger.warning('ClientResponseError: ' + str(e), exc_info=True)
            raise e
        except Exception as e:
            logger.warning('Unexpected error: ' + str(e), exc_info=True)
            raise e
