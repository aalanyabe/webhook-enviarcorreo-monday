import os
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv
from jinja2 import Environment, FileSystemLoader
from premailer import transform


load_dotenv(".env.production")

FROM_EMAIL = os.getenv("FROM_EMAIL")
APP_PASSWORD = os.getenv("APP_PASSWORD")

# Prepara Jinja
env = Environment(loader=FileSystemLoader('templates'))
template = env.get_template('encuesta.html')
def EnviarMail(cliente, idTicket, subjectTicket, email,columnIdCal,columnIdComent,idBoard,area):
    # Construir el cuerpo del mensaje HTML
    URL = os.getenv('DOMINIO_URL')
    html = template.render(
        cliente =cliente,
        idTicket = idTicket,
        subjectTicket=subjectTicket,
        url = os.getenv('DOMINIO_URL'),
        stars = {
            1: 'Muy Malo',
            2: 'Malo',
            3: 'Regular',
            4: 'Bueno',
            5: 'Excelente'
        },
        columnIdCal = columnIdCal,
        columnIdComent = columnIdComent,
        idBoard = idBoard,
        area = area
        )
    
     # Convierte todos los estilos a inline CSS
    html_inline = transform(html)
    
    # Construir el mensaje
    msg = EmailMessage()
    msg['Subject'] = f'Ticket Id {idTicket} Atendido — ¡Evalúa tu experiencia!'
    msg['From'] = f"Area de TI <{FROM_EMAIL}>"
    msg['To'] = email
    msg.set_content("Este correo contiene contenido HTML.")
    msg.add_alternative(html_inline, subtype='html')

    # Enviar usando SMTP (Gmail)
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(os.getenv("FROM_EMAIL"), os.getenv("APP_PASSWORD"))  # Contraseña de aplicación
            smtp.send_message(msg)
            print("Correo enviado exitosamente.")
            return True
    except Exception as e:
        print(f"Error al enviar correo: {e}")
        return False
