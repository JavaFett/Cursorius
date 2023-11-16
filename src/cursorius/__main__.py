import asyncio
from cursorius.telegram import TelegramCursorius


async def run_cli_tg_cursorius():
    tgc = TelegramCursorius(
        tg_template,
        'HTML',
        tg_token,
        tg_chat_id
    )

    await tgc.asend(
        instance='DEV',
        app_name='kek-application',
        message='hello world kekich',
        exc_type='ValueError',
        exc_value='kekovoe error'
    )


async def main():
    async with asyncio.TaskGroup() as task_group:
        task_group.create_task(run_cli_tg_cursorius())


if __name__ == "__main__":
    asyncio.run(main())
