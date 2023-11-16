import logging

from .telegram import TelegramCursorius
from .smtp import SMTPCursorius

__all__ = (
    "TelegramCursorius",
    "SMTPCursorius",
)


# Attach a NullHandler to the top level logger by default
# https://docs.python.org/3.10/howto/logging.html#configuring-logging-for-a-library

logging.getLogger("cursorius").addHandler(logging.NullHandler())
