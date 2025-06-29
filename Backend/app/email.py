import resend
from .config import settings

resend.api_key = settings.resend_api_key

def send_confirmation_email(to_email: str, user_name: str):
    try:
        response = resend.Emails.send({
            "from": "IDFit <noreply@flare-cloud.com>", 
            "to": [to_email],
            "subject": "פנייתך התקבלה",
            "html": f"""
                <div dir="rtl" style="text-align: right;">
                    <p>שלום {user_name},</p>
                    <p>פנייתך התקבלה בהצלחה ונחזור אליך תוך 3 ימים.</p>
                    <p>תודה,<br>צוות IDFit</p>
                    <p>--- אין להשיב למייל זה ---</p>
                </div>
            """
        })
        print("✅ Email sent:", response)
    except Exception as e:
        print("❌ Failed to send email:", repr(e))
