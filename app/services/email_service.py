import resend
from app.core.config import settings


resend.api_key = settings.resend_api_key


class EmailService:

    async def send_welcome_email(
        self,
        email: str,
        first_name: str,
    ) -> None:

        resend.Emails.send({
            "from": settings.mail_from,
            "to": [email],
            "subject": "Welcome to Blog Hub 🎉",
            "html": f"""
                <h2>Welcome to Blog Hub 🎉</h2>
                <p>Hi {first_name},</p>
                <p>Thank you for joining Blog Hub.</p>
                <p>We're excited to have you!</p>
            """
        })

    async def send_password_reset_email(
        self,
        email: str,
        reset_link: str,
    ) -> None:

        resend.Emails.send({
            "from": settings.mail_from,
            "to": [email],
            "subject": "Reset your password",
            "html": f"""
                <h2>Password Reset</h2>
                <p>You requested to reset your password.</p>
                <a href="{reset_link}">
                    Reset Password
                </a>
            """
        })