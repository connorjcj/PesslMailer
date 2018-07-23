import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

'''Sends email using a gmail account, to_addr_list will contain the farmers name, cc could just be for me and william'''
def sendemail(you, subject, message,
              login='carrfieldstechnology@gmail.com',
              password='Winter12@',
              me='carrfieldstechnology@gmail.com',
              smtpserver='smtp.gmail.com:587'):

    # Create message container - the correct MIME type is multipart/alternative.
    msgRoot = MIMEMultipart('alternative')
    msgRoot['Subject'] = subject
    msgRoot['From'] = me
    msgRoot['To'] = you

    # Encapsulate the plain and HTML versions of the message body in an
    # 'alternative' part, so message agents can decide which they want to display.
    msgAlternative = MIMEMultipart('alternative')
    msgRoot.attach(msgAlternative)

    msgText = MIMEText('This is the alternative plain text message.')
    msgAlternative.attach(msgText)

#     # We reference the image in the IMG SRC attribute by the ID we give it below
#     msgText = MIMEText('''<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
#     <html xmlns="http://www.w3.org/1999/xhtml">
#     <head>
#     <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
#     <title>Demystifying Email Design</title>
#     <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
#     </head>
#     </html>
#     <body style="margin: 0; padding: 0;">
# <table align="center" border="1" cellpadding="0" cellspacing="0" width="600" style="border: 1px solid #cccccc;">
#  <tr>
#   <td align="center" bgcolor="#70bbd9" style="padding: 40px 0 30px 0;">
#  <img src="cid:image1" alt="Creating Email Magic" width="300" height="230" style="display: block;" />
# </td>
#  </tr>
#  <tr>
#   <td bgcolor="#ffffff" style="padding: 40px 30px 40px 30px;">
#  <table border="1" cellpadding="0" cellspacing="0" width="100%">
#   <tr>
#    <td>
#     Hey it's Jim here how are ya here's the weather for the day
#    </td>
#   </tr>
#  <tr>
#   <td style="padding: 20px 0 30px 0;">
#   {}
#   </td>
#  </tr>
#   <tr>
#    <td>
#     Row 3
#    </td>
#   </tr>
#  </table>
# </td>
#  </tr>
#  <tr>
# <td>
# <iframe width="400" height="200" frameborder="1" style="border:0"
# src="https://www.google.com/maps/embed/v1/place?q=ashburton&key=AIzaSyAmBYmW9ak2SrLCEOgVEZKj5w4s3_7nSxs" allowfullscreen></iframe>
#   </td>
#  </tr>
# </table>
# '''.format(message), 'html')

    msgText = MIMEText(message, 'html')

    msgAlternative.attach(msgText)

    # Send the message via local SMTP server.
    mail = smtplib.SMTP('smtp.gmail.com', 587)

    mail.ehlo()

    mail.starttls()

    mail.login(login, password)
    mail.sendmail(me, you, msgRoot.as_string())
    mail.quit()


if __name__ == "__main__":
    me = 'carrfieldstechnology@gmail.com'
    login = 'carrfieldstechnology@gmail.com'
    password = 'Winter12@'

    you = 'connor.jaine@carrfields.co.nz'
    subject = 'Pessl Mail'
    message = 'test test test how are ya'

    sendemail(you, subject, message)
