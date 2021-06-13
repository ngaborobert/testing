from flask import Flask, render_template,request,redirect,url_for, request, redirect
import requests
import json

app = Flask(__name__)    
app.debug = True

@app.route('/')
def index():

	return render_template('index.html', title="Homepage")

@app.route('/payments', methods=['GET','POST'])
def payments():
	"""
		You need to read this information. you will get more of it from the link i sent you.
			Success Result

			{
			"success":1,
			"data": Object holding transaction receipts
			}

			Failure Result

			{“success”:0,”errormsg”:”Transaction timed out”}

			Understanding a Successful “cardpayment” Response
			{
			"success":1,
			"data": {
					"otpInfo":{
			                            "authurl":"https://..."
			                            },
					"requiresOTP":0,
					"requiresPIN":0,
					"suggestedAUTH":""
				}
			}
			If you are having an international VISA card that requires no authentication, you receive a result in the JSON format above. It is important to note that all transactions should have a pending status. The best way to truly know a transaction was completed is by using the Instant Payment Notifications as described below.

			requiresOTP

			if a value other than 0 is returned, you will need to redirect the user to a authurl provided within the otpInfo object. The easiest way would be through an IFRAME. When requiresOTP is 1, user is redirected to bank portal where he will have to confirm payment using either OTP (one time password) sent through his phone or through email.

			requiresPIN

			if requiresPIN is 1, you will have to re-post the payload above with PIN and suggestedAUTH.
			{
			"username": "your client Id",
			"password": "your secret",
			"action":"cardpayment",
			"auth":"suggestedAUTH above",
			"pin":"card pin",
			"amount":"amount in usd',
			"currency":"USD",
			"name":"name on card",
			"cardno":"card number",
			"cvv":"security code back of card",
			"month":"expiry month eg 01 for jan",
			"year":"year of expiry",
			"email":"card holders email",
			"address":"billing address",
			"city":"billing city",
			"state":"state",
			"zip":"zip code",
			"country":"billing country",
			"phone":"phone number",
			"reference":"your order reference",
			"reason":"Reason eg book payment"}

			

			Instant Payment Notification
			When a VISA payment has been successfully completed, we notify your system using the IPN url you supplied to us when enabling the API. we POST raw JSON data to you.

			The important values to note here are;

			reference – This is essentially your order id, you can now change its status to successful to match your system.

			transactionId – This is the easypay payment ID. save it to your order id in the database for cross reference.

			

			{
			"phone": "phonenumber",
			"reference": "your order id",
			"transactionId": "Easypay Transaction ID",
			"amount": "amount",
			"reason":"your reason or narrative",
			"PaymentType":"card"
			}
	"""
	if request.method == "POST":
		#you will add these validations to check if a user is putting correct information.
		amount = request.form['amount']
		name = request.form['name']
		card_no = request.form['card']
		cvv = request.form['cvv']
		month = request.form['month']
		year = request.form['year']
		email = request.form['email']
		add = request.form['address']
		city = request.form['city']
		state = request.form['state']
		zip_ = request.form['zip'] 
		country = request.form['country']
		phone = request.form['phone']
		ref = request.form['ref']
		reason = request.form['reason']

		payload = {
			"username": "a318eb06d3177320", # put that username easy pay will provide after enabling the api access.
			"password": "f9d6d5dcc88d7e7f", # same story here.
			"action":"cardpayment",
			"amount": amount,
			"currency":"UGX",
			"name": name,
			"cardno": card_no,
			"cvv": cvv,
			"month": month,
			"year": year,
			"email": email,
			"address": add,
			"city": city,
			"state": state,
			"zip": zip_,
			"country": country,  
			"phone": phone,
			"reference": ref,
			"reason": reason  
		}

		url =  "https://www.easypay.co.ug/api/"
		headers = {
    		'Content-Type': 'application/json'  
		}

		r = requests.post(url, headers=headers, data=json.dumps(payload))
	
		print(">>>>>>>>",r.status_code) # if it prints 200 or something like  that it will be indicating that the easy pay server received the request and returned a response.
		print("************",r.json) # this will be a json object with inforamtion that will indicate whether the process was successful or not.
		return redirect(url_for('payments'))
		 
	return render_template('payments.html')

if __name__ == '__main__':
	app.run(port=3000)  
  