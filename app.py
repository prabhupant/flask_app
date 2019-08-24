from flask import Flask, request
import sqlalchemy as db
import os
import json
import requests
from sqlalchemy.orm import sessionmaker
from flask_jwt import JWT, jwt_required, current_identity
from werkzeug.security import safe_str_cmp
import datetime
from flask_heroku import Heroku
from user_model import users, User

username_table = {u.username: u for u in users}
userid_table = {u.id: u for u in users}

def authenticate(username, password):
    user = username_table.get(username, None)
    if user and safe_str_cmp(user.password.encode('utf-8'), password.encode('utf-8')):
        return user

def identity(payload):
    user_id = payload['identity']
    return userid_table.get(user_id, None)


app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = 'super-secret'
app.config['JWT_EXPIRATION_DELTA'] = datetime.timedelta(days=5)

heroku = Heroku(app)

jwt = JWT(app, authenticate, identity)

engine = db.create_engine('postgres://mpjmtenfmhvgzv:81a8dc3e552c0f7f9fa2c7050b97de63c65f13f46dc88f32e134d59eb94778fc@ec2-174-129-27-3.compute-1.amazonaws.com:5432/d19a8cjvcvncvc')
metadata = db.MetaData()

connection = engine.connect()

fyle_banks = db.Table('banks', metadata, autoload=True, autoload_with=engine)
fyle_branches = db.Table('branches', metadata, autoload=True, autoload_with=engine)

Session = sessionmaker(bind=engine)
session = Session()

@app.route('/')
def index():
    return "Welcome to the app! \nPlease refer to the readme in the GitHub repo to learn more about the APIs"


@app.route('/bank')
@jwt_required()
def get_bank():
    ifsc = request.args.get('ifsc')
    if ifsc == None:
        return "Please enter the ifsc code in the query parameters"
    # Querying the database
    s = session.query(fyle_branches, fyle_banks).join(fyle_banks).filter(fyle_branches.columns.bank_id == fyle_banks.columns.id).filter(fyle_branches.columns.ifsc==ifsc).one()


    # Making a JSON out of the query result
    res = {
            'bank_name': s[7],
            'ifsc': s[0],
            'bank_id': s[1],
            'branch': s[2],
            'address': s[3],
            'city': s[4],
            'district': s[5],
            'state': s[6]
    }

    return json.dumps(res, indent=4)


@app.route('/branches')
@jwt_required()
def get_branches():
    bank = request.args.get('bank')
    city = request.args.get('city')
    limit = request.args.get('limit')
    offset = request.args.get('offset')

    if bank == None or city == None:
        return "Please enter both the bank name and the city"

    if not offset == None and not limit == None:
        offset = int(offset)
        limit = int(limit)
        limit = limit + offset

    s = session.query(fyle_branches).join(fyle_banks).\
                    filter(fyle_banks.columns.name==bank).\
            filter(fyle_banks.columns.id == fyle_branches.columns.bank_id).\
            filter(fyle_branches.columns.city==city)[offset:limit]

    res = []
    for i in s:
        j = {
                'ifsc': i[0],
                'bank_id': i[1],
                'branch': i[2],
                'address': i[3],
                'city': i[4],
                'district': i[5],
                'state': i[6]
        }
        res.append(j)

    return json.dumps(res, indent=4)

if __name__ == '__main__':
    app.run()
