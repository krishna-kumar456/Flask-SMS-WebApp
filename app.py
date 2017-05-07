import os
import random
import datetime
from flask import Flask, render_template, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


from models import Contacts, Messages

@app.route('/')
def home_page():
    return render_template("index.html")

@app.route('/contacts')
def contacts_page():
	try:
		contact = Contacts.query.all()
		print('Got Contacts')
	except Exception as e:
		print(e)

	

	return render_template('contacts.html', contact_list=contact)

@app.route('/messages')
def messages_page():
	return render_template('messages.html')

@app.route('/contactinfo/<contactname>')
def contact_info(contactname):
	contact_name = contactname
	session['current_user'] = contact_name
	row = Contacts.query.filter(Contacts.name == contact_name).first_or_404()
	contact_no = row.phone_no
	return render_template('contactinfo.html', contact_name=contact_name, contact_no= contact_no)

@app.route('/sendmessage')
def send_message():
	smstext = "“Hi. Your OTP is: "
	random_string = ''.join(["%s" % random.randint(0, 9) for num in range(0, 6)])
	smstext += random_string
	print(smstext)
	try:
		result = Messages(name=session['current_user'] , message=smstext, time=str(datetime.datetime.now()))
		db.session.add(result)
		print('Added result to session')
		db.session.commit()
		print('DB Addition Success')
	except Exception as e:
		db.session.rollback()
		print("Unable to add item to database.")
		print(e)
	finally:
		db.session.close()

	return render_template('sendmessage.html', smstext=smstext)



if __name__ == '__main__':
    app.run()