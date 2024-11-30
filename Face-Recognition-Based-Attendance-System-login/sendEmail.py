import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os
import glob

def sendEmail():
    mail_content = '''Hello,
    This is a Attendance mail.
    In this mail we are sending student attendance excel file attachments.
    
    Thank You
    '''
    #The mail addresses and password
    sender_address ='diwa.2801@gmail.com'
    sender_pass ='furgqbokcooqfjkf'
    receiver_address ='kirran231@gmail.com'
    #Setup the MIME
    message = MIMEMultipart()
    message['From'] = sender_address
    message['To'] = receiver_address
    message['Subject'] = 'A Attendance Excel File. It has an attachment.'
    #The subject line
    #The body and the attachments for the mail
    message.attach(MIMEText(mail_content, 'plain'))


    list_of_files=glob.iglob('D:/Face-Recognition-Based-Attendance-System-login/*.csv')
    latest_file = max(list_of_files, key=os.path.getctime)



    
    attach_file_name = latest_file
    attach_file = open(attach_file_name, 'rb')  # Open the file as binary mode
    payload = MIMEBase('application', 'octate-stream')
    payload.set_payload((attach_file).read())
    encoders.encode_base64(payload) #encode the attachment
    #add payload header with filename
    payload.add_header("Content-Decomposition", f"attachment; filename= {attach_file_name}",)
    message.attach(payload)
    #Create SMTP session for sending the mail
    session = smtplib.SMTP('smtp.gmail.com', 587) #use gmail with port
    session.starttls() #enable security
    session.login(sender_address, sender_pass) #login with mail_id and password
    text = message.as_string()
    session.sendmail(sender_address, receiver_address, text)
    session.quit()
    print('Mail Sent')
