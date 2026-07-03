from fastapi_mail import (
    ConnectionConfig,
    FastMail,
    MessageSchema,
    MessageType,
)

from app.core.config import settings


conf = ConnectionConfig(
    MAIL_USERNAME=settings.mail_username,
    MAIL_PASSWORD=settings.mail_password,
    MAIL_FROM=settings.mail_from,
    MAIL_PORT=settings.mail_port,
    MAIL_SERVER=settings.mail_server,
    MAIL_FROM_NAME=settings.mail_from_name,
    MAIL_STARTTLS=settings.mail_starttls,
    MAIL_SSL_TLS=settings.mail_ssl_tls,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True,
)


class EmailService:
    def __init__(self):
        self.fast_mail = FastMail(conf)

    async def send_password_reset_email(
        self,
        email: str,
        reset_link: str,
    ) -> None:
        html = f"""
        <html>
            <body>
                <h2>Password Reset</h2>

                <p>You requested to reset your password.</p>

                <p>
                    Click the button below to reset it.
                </p>

                <p>
                    <a
                        href="{reset_link}"
                        style="
                            background:#2563eb;
                            color:white;
                            padding:12px 20px;
                            text-decoration:none;
                            border-radius:6px;
                        "
                    >
                        Reset Password
                    </a>
                </p>

                <p>
                    If you didn't request this, you can safely ignore this email.
                </p>

                <p>
                    This link expires in 15 minutes.
                </p>
            </body>
        </html>
        """

        message = MessageSchema(
            subject="Reset your password",
            recipients=[email],
            body=html,
            subtype=MessageType.html,
        )

        await self.fast_mail.send_message(message)

    async def send_welcome_email(
        self,
        email: str,
        first_name: str,
    ) -> None:
        html = f"""
        <html>
            <body>
                <h2>Welcome to Blog Hub🎉</h2>

                <p>Hi {first_name},</p>

                <p>
                    Thank you for joining Blog Hub.
                </p>

                <p>
                    We're excited to have you!
                </p>
            </body>
        </html>
        """

        message = MessageSchema(
            subject="Welcome to Blog Hub🎉",
            recipients=[email],
            body=html,
            subtype=MessageType.html,
        )

        await self.fast_mail.send_message(message)