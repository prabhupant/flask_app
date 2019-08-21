# Bank fetcher

A flask app to fetch the details of a bank

* Heroky URL - `https://fylepp.herokuapp.com/`

## Tech stack used
* Flask (Python)
* Postgres

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
  https://fylepp.herokuapp.com/bank \
  -H 'Authorization: JWT <JWT TOKEN>' \
  -H 'Content-Type: application/json' \
  -d '{
	"ifsc": "ABHY0065001"
}'
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
  https://fylepp.herokuapp.com/branches \
  -H 'Authorization: JWT <JWT TOKEN>' \
  -H 'Content-Type: application/json' \
  -d '{
"bank_name": "STATE BANK OF INDIA",
"city": "LUCKNOW",
"limit": 5,
"offset": 10
}'
```

Note: The `limit` and `offset` parameters are optional. The API call will work without them also.

* Response -

```
[
    {
        "ifsc": "SBIN0002510",
        "bank_id": 1,
        "branch": "AYODHYA",
        "address": "FAIZABAD,  UTTAR PRADESH,  PIN  224123",
        "city": "LUCKNOW",
        "district": "FAIZABAD",
        "state": "UTTAR PRADESH"
    },
    {
        "ifsc": "SBIN0002593",
        "bank_id": 1,
        "branch": "PANDEY GANJ  LUCKNOW",
        "address": "GANGA PRASAD VERMA ROAD RAKABGANJ LUCKNOW,226018",
        "city": "LUCKNOW",
        "district": "LUCKNOW",
        "state": "UTTAR PRADESH"
    },
    {
        "ifsc": "SBIN0002597",
        "bank_id": 1,
        "branch": "PURANI BASTI",
        "address": "PURANI BASTI,  BASTI, UTTAR PRADESH, PIN  272002",
        "city": "LUCKNOW",
        "district": "SANT KABIR NAGAR",
        "state": "UTTAR PRADESH"
    },
    {
        "ifsc": "SBIN0003222",
        "bank_id": 1,
        "branch": "ALAMBAGH",
        "address": "SHRINGAR NAGAR LUCKNOW,226005 226005",
        "city": "LUCKNOW",
        "district": "LUCKNOW",
        "state": "UTTAR PRADESH"
    },
    {
        "ifsc": "SBIN0003223",
        "bank_id": 1,
        "branch": "NISHANT GANJ  LUCKNOW",
        "address": "FAIZABAD ROAD,NISHATGANJ LUCKNOW,LUCKNOW,226016",
        "city": "LUCKNOW",
        "district": "LUCKNOW",
        "state": "UTTAR PRADESH"
    }
]
```