from flask import Flask, render_template, request
import boto3
from boto3.dynamodb.conditions import Key, Attr

app = Flask(__name__)

@app.route('/')
def hello_world():
        return render_template('index.html')

@app.route('/load_register/', methods=["GET","POST"])
def load_register():
    return render_template(
        'register.html')

@app.route('/load_index/', methods=["GET","POST"])
def load_index():
    return render_template(
        'index.html')

@app.route('/load_VOTD/', methods=["GET","POST"])
def load_VOTD():
    return render_template(
        'votd.html')

@app.route('/load_VOG/', methods=["GET","POST"])
def load_VOG():
    return render_template(
        'vog.html')

@app.route('/load_DSC/', methods=["GET","POST"])
def load_DSC():
    return render_template(
        'dsc.html')

@app.route('/load_GOS/', methods=["GET","POST"])
def load_GOS():
    return render_template(
        'gos.html')

@app.route('/load_LW/', methods=["GET","POST"])
def load_LW():
    return render_template(
        'lw.html')

def check_email():
     email = request.form.get('email')
     username = request.form.get('username')
     password = request.form.get('password')
     dynamodb_resource = boto3.resource('dynamodb')
     table = dynamodb_resource.Table('login')
     response = table.get_item(
        Key={
        'email': email
        }
     )
     try:
        items = response['Item']
     except KeyError:
        items = ''
     if items != '':
        if password != items['password']:
           items = ''
     return dict(items)

@app.route('/check_login/', methods=["GET","POST"])
def check_login():
     emailnow = check_email()
     username = request.form.get('username')
     error = 'error login details dosent exist i.e. password or email'
     if not emailnow:
         return (error)
     else:
         return render_template('main.html', username=username)

@app.route('/check_register/', methods=["GET","POST"])
def check_register():
     username = request.form.get('username')
     email = request.form.get('email')
     password = request.form.get('password')
     dynamodb_resource = boto3.resource('dynamodb')
     table = dynamodb_resource.Table('login')
     responce0 = table.get_item(
         Key={
         'email': email
         }
     )
     try:
         items = responce0['Item']
     except KeyError:
         items = ''
     if items == '':
         response1 = table.put_item(
             Item={
             'user_name': username,
             'email': email,
             'password': password
             }
         )
         return render_template('index.html')
     else:
         return 'Error: Email Already Exists'

@app.route('/check_post/', methods=["GET","POST"])
def check_post():
    id = request.form.get('id')
    raid = request.form.get('raid')
    username = request.form.get('username')
    dynamodb_resource = boto3.resource('dynamodb')
    table = dynamodb_resource.Table('post')
    responce = table.put_item(
        Item={
        'id': id,
        'raid': raid
        }
    )
    return render_template('main.html', username = username)

@app.route('/get_post/', methods=["GET","POST"])
def get_post():
    username = request.form.get('username')
    raid = request.form.get('raid')
    if raid != "":
        dynamodb_resource = boto3.resource('dynamodb')
        table = dynamodb_resource.Table('post')
        responce = table.query(
            IndexName='raid-index',
            KeyConditionExpression=Key('raid').eq(raid))
        try:
            items = responce['Items']
        except KeyError:
            items = "Error: No Raid Posts Avalible"
    if raid == "":
        items = "Error: Null Input"
    return render_template('main.html', username = username, items = items)

if __name__ == "__main__":
         app.run()
