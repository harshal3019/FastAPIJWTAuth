from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from pydantic import BaseModel, EmailStr
conf = ConnectionConfig(
    MAIL_USERNAME="ce6c92225d3572",          # Your Mailtrap username
    MAIL_PASSWORD="995787ecae6960",          # Your Mailtrap password
    MAIL_FROM="harshal.mahajan@example.com",      # Your sender email (can be anything in Mailtrap)
    MAIL_PORT=587,                           # Port 587 for TLS
    MAIL_SERVER="smtp.mailtrap.io",          # Mailtrap's SMTP server
    MAIL_STARTTLS=True,                           # Enable TLS
    MAIL_SSL_TLS=False,                          # Disable SSL since TLS is enabled
    USE_CREDENTIALS=True,                    # Enable credentials
    VALIDATE_CERTS=True                      # Validate SSL certificates
)

# Email schema
class EmailSchema(BaseModel):
    email: EmailStr
    subject: str
    body: str
