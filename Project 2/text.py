##########################################
# Name: Jeremy Marks                     #
# Purpose: send text to given name       #
##########################################

def send_text(name, body):
    import smtplib
    if name == 'jeremy': recipient = 'MY_PHONENUMBER@MY_CARRIER_LINK.com'
    FROM = 'MY_EMAIL@gmail.com'
    TO = recipient if isinstance(recipient, list) else [recipient]
    TEXT = body

    # Prepare actual message
    message = """From: %s\nTo: %s\nSubject: %s\n\n%s
    """ % (FROM, ", ".join(TO), '', TEXT)
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.ehlo()
        server.starttls()
        server.login('MY_EMAIL@gmail.com', 'MY_PASSWORD!')
        server.sendmail(FROM, TO, message)
        server.close()
    except:
        print("Failed to send Text")