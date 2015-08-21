import json
import ujson
from flask import Flask, render_template, request, session
from tinydb import TinyDB, where
from twilio.rest import TwilioRestClient
from random import randint


app = Flask(__name__)
db = TinyDB('aalome.json')
app.config['SECRET_KEY'] = str(randint)
account_sid = "ACac4953fc8d049aca76edcfe4197c30fd"
auth_token = "216b04e2a716640cb7af02404ebea2e7"


@app.route('/', methods=['GET'])
def index_get():
    return render_template('index.html')


@app.route('/vendorinput', methods=['GET'])
def vendorinput_get():
    return render_template('vendorinput.html')


@app.route('/vendorinput', methods=['POST'])
def vendorinput_post():
    data = request.form
    address = data['address']
    phone = data['phone']
    name = data['business']
    email = data['email']
    footfall = data['footfall']
    db.insert(
        {'address': data['address'], 'phone': data['phone'], 'name': data['business'], 'footfall': data['footfall'],
         'email': data['email'], 'status': False})
    print(db.all())
    session['token'] = randint(100000, 999999)
    client = TwilioRestClient(account_sid, auth_token)
    message = client.messages.create(to=phone, from_="+14155992671",
                                     body="Please enter this code on the webpage: " + str(session['token']))
    return render_template('confirmphone.html', message="Please Enter verification code here")


@app.route('/confirmphone', methods=['POST'])
def confirmphone_post():
    if int(request.form['phone']) == session['token']:
        return render_template('confirm.html', message="Phone verification successfull")
    else:
        return render_template('confirmphone.html', message="Incorrect! Please try again")


@app.route('/notify', methods=['GET'])
def notify_get():
    return render_template('notification.html')


@app.route('/vendlist', methods=['GET'])
def vendlist_get():
    return render_template('vendlist.html', msg=json.dumps(db.all()))


@app.route('/vendsearch', methods=['GET'])
def vendsearch_get():
    return render_template('vendsearch.html')


@app.route('/vendsearch', methods=['POST'])
def vendsearch_post():
    search = request.form['business']
    result = db.search(where('name').matches('^' + search))
    return render_template('vendlist.html', msg=json.dumps(result))


@app.route('/vendor/<vid>', methods=['GET'])
def vend_get(vid):
    vend = db.get(where('phone') == vid)
    return render_template('vendor.html', msg=json.dumps(vend))


@app.route('/subscribe/<vid>', methods=['GET'])
def subscribe_get(vid):
    vend = db.get(where('phone') == vid)
    return render_template('subscribe.html', msg=json.dumps(vend), message="Please enter your phone number here",
                           id=vid)


@app.route('/subscribe', methods=['POST'])
def subscribe_post():
    vend = request.form['vendor']
    custphone = request.form['phone']
    session['token2'] = randint(100000, 999999)
    client = TwilioRestClient(account_sid, auth_token)
    message = client.messages.create(to=custphone, from_="+14155992671",
                                     body="Please enter this code on the webpage: " + str(session['token2']))
    return render_template('subconfirmphone.html', msg=json.dumps(vend), message="Please enter verification code",
                           cust=custphone)


@app.route('/subconfirmphone', methods=['POST'])
def subconfirmphone_post():
    if int(request.form['phone']) == session['token2']:
        db.insert({'custphone': request.form['custphone'], 'vendorphone': request.form['vendor']})
        custsubs = db.get(where('custphone') == request.form['custphone'])
        vends=[]
        for v in custsubs:
            vends.append(db.get(where('phone') == custsubs[v]))
        return render_template('subconfirm.html', message="Phone verification successfull. This phone is now subscribed to the following vendors.", vendors=json.dumps(filter(None, vends)))
    else:
        return render_template('subconfirmphone.html', message="Incorrect! Please try again")


if __name__ == '__main__':
    app.run(debug=True)
