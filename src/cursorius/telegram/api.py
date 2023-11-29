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

PARSE_MODE: TypeAlias = Literal["HTML", "MarkdownV2"]


class TelegramCursorius:
    """
    Delivery a message to a recipient using Telegram.

    :param str template:

    `HTML` example: "<b>[ {instance} {app_name} ]</b> \\n{message} \\n<i>{exc_type}</i> | {exc_value}"

    `MarkdownV2` example: "*[ {instance} {app_name} ]* \\n{message} \\n_{exc_type}_ \| {exc_value}"

    `Plain text` example: "[ {instance} {app_name} ] \\n{message} \\n{exc_type} | {exc_value}"

    :param str token: Telegram bot token
    :param str chat_id: Telegram chat id
    :param str parse_mode: 'HTML' or 'MarkdownV2' or None(Plain text)
    :param bool explain: By default the library does not setup any handler other than the NullHandler.
    Toggle this to True to add a StreamHandler.
    """

    def __init__(
        self,
        template: str,
        token: str,
        chat_id: str,
        parse_mode: PARSE_MODE | None = None,
        explain: bool = False
    ) -> None:
        self._template = self._validate_template(template)
        self._token = token
        self._chat_id = chat_id
        self._parse_mode = parse_mode
        self._enable_logging(explain)

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

    def _get_url(self, **kwargs) -> str:
        message = self._get_format_message(**kwargs)
        url = self._fill_url(message)

        return url

    def _get_format_message(self, **kwargs) -> str:
        try:
            result = self._template.format(**kwargs)
        except KeyError as e:
            logger.error(f'KeyError: {str(e)}', exc_info=True)
        except Exception as e:
            logger.error(f'Error: {str(e)}', exc_info=True)

        return result

    def _fill_url(self, text: str):
        url = "https://api.telegram.org/bot" + self._token \
            + "/sendMessage?chat_id=" + self._chat_id \
            + "&text=" + text \

        if self._parse_mode is not None:
            url += "&parse_mode=" + self._parse_mode

        return url

    def _validate_template(self, url):
        url = url.replace('\n', '%0A')

        return url

    def _execute_request(self, url):
        try:
            response = requests.get(url)
            response_json = response.json()
            if response.json()['ok'] is False:
                logger.warning(
                    f'Error: {response_json["error_code"]} - {response_json["description"]}')
        except Exception as e:
            logger.error(f'Error: {str(e)}', exc_info=True)

    async def _execute_request_async(self, url):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    response_json = await response.json()
                    if response_json['ok'] is False:
                        logger.warning(
                            f'Error: {response_json["error_code"]} - {response_json["description"]}')
        except Exception as e:
            logger.error(f'Error: {str(e)}', exc_info=True)

    def _enable_logging(self, explain: bool):
        if explain:
            logger.addHandler(log_handler)
