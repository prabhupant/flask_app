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

class User():
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

    
    def __str__(self):
        return 'User(id={})'.format(self.id)


users = [
    User(1, 'fyle', 'bangalore'),
    User(2, 'google', 'mountainview')
]

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

engine = db.create_engine('postgresql://postgres:postgres@localhost:5432/fyle_db')
metadata = db.MetaData()

connection = engine.connect()

fyle_banks = db.Table('banks', metadata, autoload=True, autoload_with=engine)
fyle_branches = db.Table('branches', metadata, autoload=True, autoload_with=engine)

Session = sessionmaker(bind=engine)
session = Session()


@app.route('/bank')
@jwt_required()
def get_bank():
    data = request.json
    ifsc = data['ifsc']

    # Querying the database
    s = session.query(fyle_branches, fyle_banks).join(fyle_banks).filter(fyle_branches.columns.bank_id == fyle_banks.columns.id).filter(fyle_branches.columns.ifsc==ifsc).all()

    # Making a JSON out of the query result
    res = {
            'bank_name': s[0][7],
            'ifsc': s[0][0],
            'bank_id': s[0][1],
            'branch': s[0][2],
            'address': s[0][3],
            'city': s[0][4],
            'district': s[0][5],
            'state': s[0][6]
    }
            
    return json.dumps(res, indent=4)


@app.route('/branches')
@jwt_required()
def get_branches():

    data = request.json
    bank = data['bank_name']
    city = data['city']
    limit = None
    offset = None
    if 'limit' in data:
        limit = data['limit']
    if 'offset' in data:
        offset = data['offset']

    if not offset == None:
        limit = offset + limit
    
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
