from flask_mail import Mail, Message
from flask import Flask





app=Flask(__name__)

app.config.update(
        DEBUG=True,
        MAIL_SERVER= 'smtp.gmail.com',
        MAIL_PORT=465,
        MAIL_USE_SSL=True,
        MAIL_USERNAME='godwillkisia5@gmail.com',
        MAIL_PASSWORD='godwill876'

        )

mail=Mail(app)


@app.route('/')
def sendmail():
    msg = Message('trial mail',
    sender = 'godwillkisia5@gmail.com',
    recipients=['godwilltrevor@gmail.com'])
    msg.body='welcome to gtrek solutions'
    mail.send(msg)
    return 'mail sent'




if __name__=='__main__':
    app.run(debug=True)
