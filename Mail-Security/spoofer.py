import smtplib
import socket
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from getpass import getpass

# === Configuration Section ===

smtp_server = "smtp.gmail.com"                     # SMTP server address
port = 587                                         # SMTP port (587 for TLS)
sender_email = "yourname@gmail.com"                # The real sender's email address (used for login)
from_header = "Your Name <yourname@gmail.com>"     # This appears in the "From" field
recipient_email = "friend@example.com"             # Email address of the recipient
subject = "Hello"                                  # Subject line of the email
body = "This is a test"                            # Body content of the email

# === Ask user for password securely ===

sender_password = getpass("Enter sender email password: ")

# === Compose the email ===

message = MIMEMultipart()
message['From'] = from_header
message['To'] = recipient_email
message['Subject'] = subject
message.attach(MIMEText(body, 'plain'))

try:
    print(f"[*] Connecting to SMTP server {smtp_server}:{port}...")
    server = smtplib.SMTP(smtp_server, port, timeout=10)
    print("[+] Connected.")

    print("[*] Starting TLS encryption...")
    server.starttls()
    print("[+] Connection secured.")

    print("[*] Logging in as", sender_email)
    server.login(sender_email, sender_password)
    print("[+] Login successful.")

    print("[*] Sending email...")
    server.sendmail(sender_email, recipient_email, message.as_string())
    print(f"[+] Email successfully sent to {recipient_email}!")

    print("\n--- Summary ---")
    print(f"SMTP Server : {smtp_server}:{port}")
    print(f"Sender      : {sender_email}")
    print(f"From Header : {from_header}")
    print(f"Recipient   : {recipient_email}")
    print(f"Subject     : {subject}")
    print(f"Body        : {body}")

except socket.timeout:
    print("[!] ERROR: Connection timed out. Check SMTP server or network.")
except smtplib.SMTPAuthenticationError:
    print("[!] ERROR: Authentication failed. Check email or password.")
except Exception as e:
    print("[!] ERROR:", e)
finally:
    if 'server' in locals() and server.sock:
        server.quit()
        print("[*] SMTP connection closed.")
