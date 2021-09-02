import commands
fromaddr = "gokul.hp.vijay@gmail.com"
passwd = "9894271752"
toaddr = "gokulvijayskr@gmail.com"
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
msg = MIMEMultipart()
def sendMail():
    print("Send Mail Started")
    try:
        print("Taking Picture")
        commands.getoutput(r'fswebcam -r 1280x720 /home/pi/Desktop/MotionDetection/Image/lastPicture.jpg')
    except:
        print("Error to Take Picture")
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = "Cam Activated"
    body = "Motion Detected "
    msg.attach(MIMEText(body, 'plain'))
    import os
    #rootpath = '/home/pi/Desktop/Image'
    rootpath = '/home/pi/Desktop/MotionDetection/Image'
    filelist = [os.path.join(rootpath, f) for f in os.listdir(rootpath)]
    filelist = [f for f in filelist if os.path.isfile(f)]
    newest = max(filelist, key=lambda x: os.stat(x).st_mtime)
    filename = newest
    #print(filename)
    import os
    #rootpath = '/home/pi/Desktop/Image'
    rootpath = '/home/pi/Desktop/MotionDetection/Image'
    filelist = [os.path.join(rootpath, f) for f in os.listdir(rootpath)]
    filelist = [f for f in filelist if os.path.isfile(f)]
    newest = max(filelist, key=lambda x: os.stat(x).st_mtime)
    #print(newest)
    attachment = open(newest, "rb")
    part = MIMEBase('application', 'octet-stream')
    part.set_payload((attachment).read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', "attachment; filename= %s" % filename)
    msg.attach(part)
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(fromaddr, passwd)
    text = msg.as_string()
    server.sendmail(fromaddr, toaddr, text)
    server.quit()
    print("Mail Sent")
    print("Waiting for next Move in PIR Sensor")


import time
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(14, GPIO.IN)
print("Program Started Keep sensor alone")
while True:
    if(GPIO.input(14)):
        time.sleep(0.1)
        if(GPIO.input(14)):
            print("Motion Detected")
            sendMail()

