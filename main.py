import smtplib
import json
import time


def main():
    global passwort
    passwort = ""
    print("\nPlease choose a Number")
    aktion = input("""[1] Login
[2] Send Email
[3] Show last Account\n""")
    if aktion == "1":
        add_account()
    if aktion == "2":
        send_email()
    if aktion == "3":
        with open("data.json", "r") as file:
            data = json.load(file)
            user = data["Account"]["email"]["passwort"]
            print(user)


def add_account():
    print("""⚠️ | Account not activated:
Please disable this to be able to send Emails from your Account
https://myaccount.google.com/lesssecureapps?pli=1&rapt=AEjHL4MKTxvoEfLGAXVtZcG2X-Km2BiN6qpEQVfHplvAk6QLsgy43zbRxS_OBE34b8Jq04rSxYfD5R4lNsFDlj-lFBiZ8eD_ng""")

    email = input("⚠️ | Please enter your Gmail address\n").replace(" ", "")
    passwort = input(
        "⚠️ | Please enter your password\n").replace(
        " ", "*")
    with open("data.json", "r") as file:
        data = json.load(file)

    with open("data.json", "w") as file:
        data.setdefault("Account", {}).update({"email": email})
        json.dump(data, file)


def send_success_email(email_suc, status):
    with open("data.json", "r") as file:
        data = json.load(file)
        user = data["Account"]["email"]

    if status:
        subject = f"""Email successfully sent to: {email_suc}"""
        mail_text = "email was send!"

    else:
        subject = f"""Email to Client {email_suc} failed"""
        mail_text = "⚠️ | Email failed, please try again."

    mail_from = 'test@example.com'
    rcpt_to = user
    data = 'From:%s\nTo:%s\nSubject:%s\n\n%s' % (mail_from, rcpt_to, subject, mail_text)
    server = smtplib.SMTP('smtp.gmail.com:587')
    server.starttls()
    server.login(user, passwort)
    server.sendmail(mail_from, user, data)
    server.quit()


def send_email():
    global passwort
    if passwort == "":
        passwort = input(

            "⚠️ | Please enter your password\n").replace(

            " ", "*")
    with open("data.json", "r") as file:
        data = json.load(file)
        user = data["Account"]["email"]

    with open("text.txt", "r") as mes:
        mail_text = mes.read()
    subject = input("⚠️ | Please enter the reference\n")

    mail_from = 'test@example.com'
    rcpt_to = input("❓ | Where should we Email send to? Separate multiple users with commas.\n").replace(" ", "").split(
        ",")
    data = 'From:%s\nTo:%s\nSubject:%s\n\n%s' % (mail_from, rcpt_to, subject, mail_text)

    if input("⚠️ | Should we really send this? (y/N)\n").replace(" ", "").lower() == "y":
        for i in range(0, 80):
            print("=", end="")
            time.sleep(0.01)

        for email in rcpt_to:
            try:
                server = smtplib.SMTP('smtp.gmail.com:587')
                server.starttls()
                server.login(user, passwort)
                server.sendmail(mail_from, email, data)
                server.quit()
                print(f"""\n✅ | Email to {email} successfully sent""")
                status = True
            except:
                print("\n⚠️ | Error while sending Email")
                status = False
            try:
                send_success_email(email, status)
            except:
                print("\n⚠️ | Error while sending confirmation email.")
    else:
        print("\n💢 | Cancelled.")


if __name__ == '__main__':
    while True:
        main()
