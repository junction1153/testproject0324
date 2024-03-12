#!/usr/bin/python3
# -*- coding: utf-8 -*-

import subprocess
import smtplib
import time
from email.mime.text import MIMEText

# Function to send email
def send_email(subject, body):
    sender_email = "noreply@jc.com"
    sender_email = "Junction Cloud <noreply@jc.com>"
    receiver_email = ['ja@jc.com']
    subject = "PBX99 Alert"
    smtp_user = "username"
    password = "password"


    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender_email
#    msg['To'] = receiver_email
    msg['To'] = ", ".join(receiver_email)

    with smtplib.SMTP('smtp.postmarkapp.com', 587) as server:
        server.starttls()
        server.login(smtp_user, password)
        server.sendmail(sender_email, receiver_email, msg.as_string())

def check_sip_server():
    success_count = 0
    failure_count = 0
    server_up = False

    for _ in range(3):
        try:
            # Execute curl command
            result = subprocess.run(["curl", "--max-time", "5", "-X", "POST", "-H", "Content-Type: application/json", "-d", '{"hostIp":"IP_Address_Here","hostPort":"5060"}', "http://localhost:3000/sipsak"], capture_output=True, text=True, timeout=10)

            # Check if SIP server is available
            if "SIP server is AVAILABLE" in result.stdout:
                success_count += 1
                failure_count = 0
            else:
                failure_count += 1
                success_count = 0

            if success_count == 3:
                server_up = True
                break
            elif failure_count == 3:
                server_up = False
                break
        except Exception as e:
            print(f"Error: {e}")
            failure_count += 1
            success_count = 0

        # Wait for 300 seconds before next attempt
        time.sleep(300)

    return server_up

def main():
    server_up = False

    while True:
        new_server_up = check_sip_server()
        if new_server_up != server_up:
            if new_server_up:
                send_email("SIP Service Restored", "PBX99 Conf is successfully responding to SIP OPTIONS")
            else:
                send_email("SIP Service Failure", "PBX99 Conf IS NOT responding to SIP OPTIONS")
            server_up = new_server_up

if __name__ == "__main__":
    main()
