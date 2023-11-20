import logging
import smtplib
import asyncio
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


logger = logging.getLogger("cursorius")
log_handler = logging.StreamHandler()
log_handler.setFormatter(
    logging.Formatter(
        "{asctime} | {name} | {levelname} | {message}", style="{")
)
logger.addHandler(log_handler)


class SMTPCursorius:
    def __init__(self, smtp_server, smtp_port, sender_email, sender_password):
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.sender_email = sender_email
        self.sender_password = sender_password

    def _create_message(self, recipient_email, subject, template_content):
        message = MIMEMultipart()
        message['From'] = self.sender_email
        message['To'] = recipient_email
        message['Subject'] = subject
        message.attach(MIMEText(template_content, 'plain'))
        return message

    def _send_email(self, recipient_email, subject, template_content):
        message = self._create_message(
            recipient_email, subject, template_content)

        with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
            server.starttls()
            log_in = server.login(self.sender_email, self.sender_password)
            logger.warning(log_in)
            server.send_message(message)

    def send_message(self, recipient_email, subject, template_content):
        self._send_email(recipient_email, subject, template_content)

    async def send_message_async(self, recipient_email, subject, template_content):
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, self._send_email, recipient_email, subject, template_content)
