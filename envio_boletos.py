import datetime
import locale
import os
import smtplib

from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

# Tradução do mês
locale.setlocale(locale.LC_TIME, 'pt_BR.UTF-8')
now = datetime.datetime.now()
data_boleto = now.strftime("%B/%Y")
nome_arquivo = now.strftime("%Y%m")

to_addr = ["exemple@email.com", "exemple@email.com", "exemple@email.com"]
acc_addr = 'exemple@email.com'
subject = 'Boleto mensal'
body = f'<p>Bom dia!</p> \
        <p>Segue o boleto conforme combinado para a mensalidade de {data_boleto}.</p> \
        <p>Atenciosamente.</p>'
signature = '<p>Everlon Passos (www.everlon.com.br)<br> \
            Desenvolvedor PHP/Python Full Stack<br> \
            programador@everlon.com.br<br> \
            Celular: 35 991 916 778 (Vivo)<br> \
            <b>EchoWorks (www.echoworks.com.br)</b></p>'

# Configura o servidor de envio (SMTP)
server = smtplib.SMTP('server-email.com', 999)
server.starttls()
server.login('exemple@email.com', 'password-strong')

# Dados do email
msg = MIMEMultipart()
msg["From"] = acc_addr
msg["To"] = ", ".join(to_addr)
msg["CC"] = 'exemple@email.com'
msg["Subject"] = subject

# Verificar arquivos dentro da pasta boletos
for file in os.listdir("boletos"):
    if file.endswith(".pdf"):

        if file.startswith(nome_arquivo) and not file.__contains__('_enviado'):

            with open('boletos/'+file, 'rb') as f:
                msgPDF = MIMEApplication(f.read(), _subtype="pdf", name='boleto-imobe-'+file)
                msg.attach(msgPDF)

                # Anexa o corpo do email
                msgText = MIMEText('{}<br>{}'.format(body, signature), 'html')
                msg.attach(msgText)

                # Envia!
                server.sendmail(acc_addr, to_addr, msg.as_string())
                print('E-Mail enviado!')
                server.quit()

                # Registra no LOG
                with open('envio_boletos.log', 'a') as f:
                    f.write(now.strftime("%d-%m-%Y")+': '+data_boleto)
                    f.write('\n')

                # Troca o nome do arquivo para definir enviados
                fenviado = file.replace(nome_arquivo, nome_arquivo+"_enviado")
                os.rename(r'boletos/'+file,r'boletos/'+fenviado)

print("Tarefa executada! Obrigado.")
