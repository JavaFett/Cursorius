import logging


def set_logging_handler(
    name: str = "cursorius",
    level: int = logging.WARNING,
    format_string: str = "{asctime} | {name} | {levelname} | {message}",
) -> None:
    logger = logging.getLogger(name)
    logger.setLevel(level)

    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter(format_string, style="{"))
    logger.addHandler(handler)
