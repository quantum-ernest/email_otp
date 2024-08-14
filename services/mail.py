from config.env import envConfig
from fastapi import HTTPException, status
from fastapi_mail import ConnectionConfig, FastMail, MessageSchema


class MailService:
    def __init__(self):
        self.config = ConnectionConfig(
            MAIL_USERNAME=envConfig.MAIL_USERNAME,
            MAIL_PASSWORD=envConfig.MAIL_PASSWORD,
            MAIL_FROM_NAME=envConfig.MAIL_FROM_NAME,
            MAIL_FROM=envConfig.MAIL_FROM,
            MAIL_PORT=envConfig.MAIL_PORT,
            MAIL_SERVER=envConfig.MAIL_SERVER,
            MAIL_STARTTLS=envConfig.MAIL_STARTTLS,
            MAIL_SSL_TLS=envConfig.MAIL_SSL_TLS,
            USE_CREDENTIALS=envConfig.MAIL_USE_CREDENTIALS,
            VALIDATE_CERTS=envConfig.MAIL_VALIDATE_CERTS,
        )

    async def send_mail(self, message: MessageSchema) -> bool:
        try:
            mail_service = FastMail(self.config)
            await mail_service.send_message(message)
            return True
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Unable to send mail: {e}",
            )
