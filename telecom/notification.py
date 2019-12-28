import smtplib
from email.mime.text import MIMEText
import os

# Useful gotcha 
# 1. If the authenticaltions are getting rejected 
#  	a) Turn on less secure apps settings -- https://myaccount.google.com/lesssecureapps 
# 	b) use the unlock URL -- https://accounts.google.com/DisplayUnlockCaptcha

# Send mail/ message allerts
# Note you can also send text messages through SMS gateway of destination number. Look here for your SMS gateway https://en.wikipedia.org/wiki/SMS_gateway
def send_message(to_addr, msg_subject, msg_body):
	if to_addr is None:
		return
	# bot configs
	from_addr = 'robot.pings@gmail.com'
	from_addr_password = 'pingingbot'

	# construct message
	msg = MIMEText(msg_body)
	msg['Subject'] = msg_subject
	msg['From'] = from_addr
	msg['To'] = to_addr

	# Establish a secure session with gmail's outgoing SMTP server using your gmail account
	server = smtplib.SMTP( "smtp.gmail.com", 587 )
	server.starttls()

	# login and send message
	server.login(from_addr, from_addr_password)
	server.sendmail(from_addr, to_addr, msg.as_string() )
	print('Message titled "%s" sent to %s' %(msg_subject, to_addr))


if __name__ == '__main__':

	# Example for sending email
	# send_message(os.environ['USER']+'@google.com', 'test subject', 'test body')
	send_message('vikashplus@gmail.com', 'test subject', 'test body')

	# Example for sending texts
	# NOTE: add your SMS gateway https://en.wikipedia.org/wiki/SMS_gateway to bash profile for this to work
	# For a project Fi number it will look like: export SMS_GATEWAY="2067348570@msg.fi.google.com"
	if "SMS_GATEWAY" in os.environ:
		send_message(os.environ['SMS_GATEWAY'], 'test subject', 'test body')
	else:
		print("Sucks")



# NOTES:
# 1) This also looks interesting: https://github.com/CrakeNotSnowman/Python_Message

