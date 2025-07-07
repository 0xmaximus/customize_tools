import smtplib
import socket  # For handling connection timeouts
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_email():
    # === SMTP Configuration ===
    smtp_server = 'smtp.gmail.com'         # SMTP server (e.g., smtp.gmail.com)
    port = 587                             # Port number for TLS
    sender_email = 'yourname@gmail.com'    # Real sender email address (used for authentication)
    sender_password = 'your_app_password'  # App-specific password or real email password

    # === Email Details ===
    from_header = 'Display Name <yourname@gmail.com>'   # This will appear in the "From" field
    recipient_email = 'friend@example.com'               # Receiver's email address
    subject = 'Hello'                                    # Email subject
    body = 'This is a test'                              # Body content of the email

    # === Create the Email Message ===
    message = MIMEMultipart()
    message['From'] = from_header
    message['To'] = recipient_email
    message['Subject'] = subject
    message.attach(MIMEText(body, 'plain'))

    try:
        print(f"[*] Connecting to SMTP server: {smtp_server}:{port}...")
        server = smtplib.SMTP(smtp_server, port, timeout=10)  # Connect with 10 seconds timeout
        print("[+] Connected successfully.")

        print("[*] Starting TLS encryption...")
        server.starttls()  # Secure the connection
        print("[+] TLS encryption established.")

        print("[*] Logging in as sender...")
        server.login(sender_email, sender_password)
        print("[+] Login successful.")

        print("[*] Sending email...")
        server.sendmail(sender_email, recipient_email, message.as_string())
        print("[+] Email sent successfully!")

    except socket.timeout:
        print("[!] ERROR: Connection timed out. SMTP server might be unreachable or blocked.")
    except smtplib.SMTPAuthenticationError:
        print("[!] ERROR: Authentication failed. Please check your email and password.")
    except Exception as e:
        print("[!] ERROR: An unexpected error occurred:", e)

    finally:
        if 'server' in locals() and server.sock:
            server.quit()
            print("[*] SMTP connection closed.")

# === Run the function ===
if __name__ == "__main__":
    send_email()
