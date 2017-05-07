"""
References
----------
* https://realpython.com/blog/python/flask-by-example-part-1-project-setup/

Author
------
Krishna Kumar

"""
import os
import random
import datetime
from flask import Flask, render_template, session, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy

#App and config initializations
app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


#Database initialization through SQLAlchemy
db = SQLAlchemy(app)

#Table Object imports
from models import Contacts, Messages


@app.route('/')
def home_page():
	""" Welcome Page to the Contact's App
	Render's initial page providing links to Contact's and Message's tab.
	"""
	return render_template("index.html")



@app.route('/contacts')
def contacts_page():
	""" Lists the contact list.
 	Fetches the contact list from the database, the list is iterated within the
 	template. 
	"""
	try:
		contact = Contacts.query.all()
		print('Got Contacts')
	except Exception as e:
		print(e)		

	return render_template('contacts.html', contact_list=contact)



@app.route('/contactadd', methods=['GET', 'POST'])
def contact_add():
	""" Helper page to add contacts while on Heroku.
	
	"""
	if request.method == "POST":

		try:
			print('Inside try')
			name = request.form['inputn']
			phone_no = request.form['inputp']
			print(name, phone_no)
			row = Contacts(name=name, phone_no=phone_no)
			db.session.add(row)
			print('Added result to session')
			db.session.commit()
			print('DB Addition Success')

		except Exception as e:
			db.session.rollback()
			print("Unable to add item to database.")
			print(e)
			

		finally:
			db.session.close()

	return render_template('contactadd.html')


@app.route('/delete')
def delete():
	""" Delete table entries for cleanup. 
	"""
	try:
		Contacts_deleted = db.session.query(Contacts).delete()
		Messages_deleted = db.session.query(Messages).delete()
		db.session.commit()
	except:
		db.session.rollback()

	return 'Deleted' + str(Contacts_deleted) + 'contacts and'+ str(Messages_deleted) + 'messages'



@app.route('/messages')
def messages_page():
	""" Display messages in descending order from the Messages Table. 
	Retrieved list of messages is iterated within the template. 
	"""
	try:
		result = Messages.query.order_by(Messages.time.desc()).all()
		print(result)
		
	except Exception as e:
		print(e)
	return render_template('messages.html', message_list=result)



@app.route('/contactinfo/<contactname>')
def contact_info(contactname):
	""" Displays contact info for the contact referenced on Contacts tab. 
	Retrieves contact info from the Contacts Table. 

	Keyword Arguments:
	contactname -- Used to received contact name from the contacts reference. 
	"""
	contact_name = contactname

	#Adding contact_name to a key in session for reference while sending a message.
	session['current_user'] = contact_name
	row = Contacts.query.filter(Contacts.name == contact_name).first_or_404()
	contact_no = row.phone_no
	return render_template('contactinfo.html', contact_name=contact_name, contact_no= contact_no)



@app.route('/sendmessage')
def send_message():
	""" Adds contact details to the backend while sending a dummy SMS. 
	"""
	smstext = "Hi. Your OTP is: "
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
		return render_template('error.html', error=e)

	finally:
		db.session.close()

	return render_template('sendmessage.html', smstext=smstext)



if __name__ == '__main__':
    app.run()