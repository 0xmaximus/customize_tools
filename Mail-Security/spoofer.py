import smtplib
import socket  # Import socket to catch the timeout error specifically
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from getpass import getpass

def send_email(sender_email, sender_password, recipient_email, subject, body):
    try:
        smtp_server = 'mail.target.com'
        port = 587

        message = MIMEMultipart()
        message['From'] = "test@target.com"
        message['To'] = recipient_email
        message['Subject'] = subject
        message.attach(MIMEText(body, 'plain'))

        print(f"[*] Attempting to connect to {smtp_server} on port {port}...")
        # ADDED a timeout of 10 seconds
        server = smtplib.SMTP(smtp_server, port, timeout=10)
        print("[+] Connection successful.")

        print("[*] Upgrading connection to TLS...")
        server.starttls()
        print("[+] Connection is now secure.")

        print("[*] Logging in...")
        server.login(sender_email, sender_password)
        print("[+] Login successful.")

        print("[*] Sending email...")
        server.sendmail(sender_email, recipient_email, message.as_string())
        print("[+] Email sent successfully!")

    # CATCH the specific timeout error
    except socket.timeout:
        print("[!] ERROR: The connection timed out. The server is unreachable or a firewall is blocking port 587.")
    except smtplib.SMTPAuthenticationError:
        print("[!] ERROR: Authentication failed. Check your username and password.")
    except Exception as e:
        print("[!] An unexpected error occurred:", e)

    finally:
        # Make sure to quit the server connection if it was established
        if 'server' in locals() and server.sock:
            server.quit()
            print("[*] Server connection closed.")

if __name__ == "__main__":
    sender_email = "user@target.com"
    sender_password = getpass("Enter your email password: ")
    recipient_email = input("Enter recipient's email address: ")
    subject = input("Enter email subject: ")
    body = input("Enter email body: ")

    send_email(sender_email, sender_password, recipient_email, subject, body)
