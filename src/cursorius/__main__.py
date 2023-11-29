import asyncio
import os
from cursorius.smtp import SMTPCursorius
from cursorius.telegram import TelegramCursorius
from cursorius.utils import set_logging_handler


NOTIFICATIONS_TELEGRAM_TOKEN = os.getenv('NOTIFICATIONS_TELEGRAM_TOKEN')
NOTIFICATIONS_TELEGRAM_RECEIVER_ID = os.getenv(
    'NOTIFICATIONS_TELEGRAM_RECEIVER_ID')
TEMPLATE_TELEGRAM_MESSAGE = "<b>[ {instance} {app_name} ]</b> \n{message} \n<i>{exc_type}</i> | {exc_value}"

SMTP_SERVER = os.getenv('SMTP_SERVER')
SMTP_PORT = os.getenv('SMTP_PORT')
SENDER_EMAIL = os.getenv('SENDER_EMAIL')
SENDER_PASSWORD = os.getenv('SENDER_PASSWORD')


async def run_cli_tg_cursorius():
    tgc = TelegramCursorius(
        TEMPLATE_TELEGRAM_MESSAGE,
        NOTIFICATIONS_TELEGRAM_TOKEN,
        NOTIFICATIONS_TELEGRAM_RECEIVER_ID,
        'HTML',
        explain=True
    )

    await tgc.send_async(
        instance='ASYNC',
        app_name='TestApplication',
        message='Syntax error in Hell0 World',
        exc_type='SyntaxError',
        exc_value='Invalid syntax',
    )

    tgc.send(
        instance='SYNC',
        app_name='TestApplication',
        message='Syntax error in Hell0 World',
        exc_type='SyntaxError',
        exc_value='Invalid syntax',
    )


async def run_cli_smtp_cursorius():
    smtpc = SMTPCursorius(
        SMTP_SERVER,
        SMTP_PORT,
        SENDER_EMAIL,
        SENDER_PASSWORD
    )

    await smtpc.send_message_async(
        'test@gmail.com',
        'Test message',
        'Hello world!'
    )


async def main():
    await run_cli_tg_cursorius()
    await run_cli_smtp_cursorius()


if __name__ == "__main__":
    asyncio.run(main())
