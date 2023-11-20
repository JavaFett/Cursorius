import asyncio
import os
from cursorius.smtp import SMTPCursorius
from cursorius.telegram import TelegramCursorius


NOTIFICATIONS_TELEGRAM_TOKEN = os.getenv('NOTIFICATIONS_TELEGRAM_TOKEN')
NOTIFICATIONS_TELEGRAM_RECEIVER_ID = os.getenv(
    'NOTIFICATIONS_TELEGRAM_RECEIVER_ID')

TEMPLATE_TELEGRAM_MESSAGE = "<b>[{instance}] [ {app_name} ]</b><br> {message}<br> {exc_type} | {exc_value}"

SMTP_SERVER = os.getenv('SMTP_SERVER')
SMTP_PORT = os.getenv('SMTP_PORT')
SENDER_EMAIL = os.getenv('SENDER_EMAIL')
SENDER_PASSWORD = os.getenv('SENDER_PASSWORD')


async def run_cli_tg_cursorius():
    tgc = TelegramCursorius(
        TEMPLATE_TELEGRAM_MESSAGE,
        'HTML',
        NOTIFICATIONS_TELEGRAM_TOKEN,
        NOTIFICATIONS_TELEGRAM_RECEIVER_ID
    )

    await tgc.send_async(
        instance='DEV',
        app_name='Test-application',
        message='Syntax error in \'Hell0 World!\'!',
        exc_type='SyntaxError',
        exc_value='Invalid syntax'
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
