# Bank fetcher

A flask app to fetch the details of a bank

* Heroky URL - `https://fylepp.herokuapp.com/`

## Tech stack used
* Flask (Python)
* Postgres

## Local installation

Clone the repo

```bash
$ git clone https://github.com/prabhupant/flask_app.git
```

`cd` into the directory and make a virtual environment and install the requirements

```bash
$ cd flask_app
$ python3 -m venv venv
$ source venv/bin/activate
$ pip3 install -r requirements.txt
```

Now setup the environment variables

```bash
$ source .env
```

Run the server

```bash
$ python3 app.py
```

## Authentication for JWT Token

* Request -
```
curl -X POST \
  https://fylepp.herokuapp.com/auth \
  -H 'Content-Type: application/json' \
  -d '{
	"username": "fyle",
	"password": "bangalore"
}'
```

* Response
```
{
    "access_token": "<JWT TOKEN>"
}
```

## Getting Bank detail by IFSC

* Request -
```
curl -X GET \
  'https://fylepp.herokuapp.com/bank/ABHY0065001' \
  -H 'Authorization: JWT <JWT TOKEN>' \
  -H 'Content-Type: application/json' \
```
Here, you can change "ABHY0065001" to any IFSC you like.

* Response -
```
{
    "bank_name": "ABHYUDAYA COOPERATIVE BANK LIMITED",
    "ifsc": "ABHY0065001",
    "bank_id": 60,
    "branch": "RTGS-HO",
    "address": "ABHYUDAYA BANK BLDG., B.NO.71, NEHRU NAGAR, KURLA (E), MUMBAI-400024",
    "city": "MUMBAI",
    "district": "GREATER MUMBAI",
    "state": "MAHARASHTRA"
}
```


## Getting branches by bank name and city

* Request -
```
curl -X GET \
  'https://fylepp.herokuapp.com/branches/STATE%20BANK%20OF%20INDIA/LUCKNOW?limit=5&offset=1' \
  -H 'Authorization: JWT <JWT TOKEN>' \
  -H 'Content-Type: application/json'
}'
```

Note: The `limit` and `offset` parameters are optional. The API call will work without them also.

* Response -

```
[
    {
        "ifsc": "SBIN0001089",
        "bank_id": 1,
        "branch": "CHARBAGH",
        "address": "DIST  LUCKNOW, UTTAR PRADESH 226001",
        "city": "LUCKNOW",
        "district": "LUCKNOW",
        "state": "UTTAR PRADESH"
    },
    {
        "ifsc": "SBIN0001100",
        "bank_id": 1,
        "branch": "CHOWK BAZAR",
        "address": "KHUNKHUNJI ROADCHOWK , LUCKNOW, UTTAR PRADESH 226003",
        "city": "LUCKNOW",
        "district": "LUCKNOW",
        "state": "UTTAR PRADESH"
    },
    {
        "ifsc": "SBIN0001132",
        "bank_id": 1,
        "branch": "CANTT LUCKNOW",
        "address": "DISTLUCKNOW  UTTAR PRADESH 226002",
        "city": "LUCKNOW",
        "district": "LUCKNOW",
        "state": "UTTAR PRADESH"
    },
    {
        "ifsc": "SBIN0001474",
        "bank_id": 1,
        "branch": "BISHESHWARGANJ",
        "address": "BISHESWAR GANJ, VARANASI, PIN 221001, U.P.",
        "city": "LUCKNOW",
        "district": "VARANASI",
        "state": "UTTAR PRADESH"
    },
    {
        "ifsc": "SBIN0001526",
        "bank_id": 1,
        "branch": "AMINABAD",
        "address": "DISTLUCKNOW  UTTAR PRADESH 226001",
        "city": "LUCKNOW",
        "district": "LUCKNOW",
        "state": "UTTAR PRADESH"
    }
]
```