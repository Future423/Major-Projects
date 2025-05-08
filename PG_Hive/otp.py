import smtplib
import random

def generate_and_send_otp(user_email):
    try:
        otp_code = str(random.randint(1000, 9999))

        subject = "Your PG Hive OTP Code"
        body = f"""Hello,

We received a request to verify your email for PG Hive.

Your One-Time Passcode (OTP): {otp_code}  

Please enter this code within 10 minutes to complete the verification process.

This is an automated email. Please do not reply.

Best Regards,  
PG Hive Team  
"""

        message = f"Subject: {subject}\n\n{body}"

        sender_email = "abcd@gmail.com"
        sender_password = "abcd efgh ijkl mnop"  # App Password
        smtp_server = "smtp.gmail.com"
        smtp_port = 587

        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, user_email, message)

        return otp_code  # Return the OTP
    except Exception as e:
        print("Error sending OTP:", e)
        return None  # In case of failure
