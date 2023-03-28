from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
import tracemalloc
tracemalloc.start()


async def send_email(nombre,destinatario):
    message = "Hola Bienvenido {}, Es un gusto darte la bienvenida a esta empresa, que ya es tu nueva familia".format(nombre)
    subject = "Bienvenido  a Technology Store"
    message = 'Subject: {}\n\n{}'.format(subject, message)
    server = smtplib.SMTP('smtp.outlook.com',587)
    server.starttls()
    server.login("jinjadepython@outlook.com","Futbol26")

    server.sendmail("jinjadepython@outlook.com", destinatario,message)
    server.quit()