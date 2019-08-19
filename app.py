from flask import Flask
import sqlalchemy as db
import os
import json
import requests

app = Flask(__name__)

engine = db.create_engine('postgresql://postgres:postgres@localhost:5432/fyle_db')
metadata = db.MetaData()

connection = engine.connect()

fyle_banks = db.Table('banks', metadata, autoload=True, autoload_with=engine)
fyle_branches = db.Table('branches', metadata, autoload=True, autoload_with=engine)


@app.route('/bank')
def get_bank():
    query = db.select([fyle_banks, fyle_branches]).where(fyle_branches.columns.ifsc=='ABHY0065001')
    print(str(query))
    res = connection.execute(query)
    res_set = res.fetchall()
    final = []
    for bank in res_set:
        final.append(bank)
    return str(final)



@app.route('/branches')
def get_branches():
    query = db.select([fyle_branches]).where(fyle_banks.columns.name=='STATE BANK OF INDIA' and fyle_branches.columns.city=='LUCKNOW')
    res = connection.execute(query)
    res_set = res.fetchall()
    return str(res_set)

if __name__ == '__main__':
    app.run()
