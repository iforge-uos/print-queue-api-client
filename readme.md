# iForge Print Queue API Client [![Version](https://badgen.net/pypi/v/print-queue-api-client/)](https://pypi.org/project/print-queue-api-client/)[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)


## About
This is the repository for the iForge Print Queue API Client. This client is used to interact with the iForge Print Queue API. The API is used to manage print jobs, printers and users in the iForge Print Queue.

## Installation
To install the client, run the following command:

```bash
(.venv): pip install print_queue_api_client
```
## Basic Usage
To use the client, import the client and create an instance of the client. The client requires a valid API key to be passed in. The API key can be obtained from the iForge Print Queue API.

It is important to note, we employ a standardised Requests response in the following form:
```python
"""
iForge Interpreted Response Standards:
{
    "error": True/False,
    "data": {{ Success-specific data (eg application) / None or optional error payload }},
    "message": {{ None or optional success message / Error-specific data (eg debug) }}
}

:return (bool error, str data, str message):
"""
```

This means that to access/use the data from a response, the 'data' key must be used. The 'data' for all `get()` functions is internally converted to a dataframe, resulting in the following recommended usage: 

```python
import print_queue_api_client as api

# create database object
db = api.database_api_factory(
    api_key="YOUR_API_KEY",
    server_ip="YOUR_SERVER_IP",
    server_port="YOUR_SERVER_PORT",
)

users = db.users.get()['data']
"""
users = {
            'error': {bool} False
            'data': {DataFrame: (1,15)}
                        completed_count date_added                          ... user_level  user_score
                    0   0               2022-12-15T16:03:34.783852+00:00    ... insane      658
                        [1 rows x 15 columns]
            'message': None
        }
"""

resp = db.users.create(name='Dom RG',
                       email='notarealemail@test.com',
                       short_name='Dom RG',
                       user_score=999,
                       is_rep=True,
                       score_editable=True)
"""
resp = {
            'error': False
            'data': 'success'
            'message': None
        }
"""

```
## Documentation
### Example usage
```python
import logging
import pandas as pd
import os
from dotenv import load_dotenv, find_dotenv
import print_queue_api_client as api

logging.basicConfig()
logging.getLogger().setLevel(logging.ERROR)

pd.set_option('display.max_columns', 4)

load_dotenv(find_dotenv())
SERVER_IP = os.getenv("SERVER_IP")
SERVER_PORT = os.getenv("SERVER_PORT")
API_KEY = os.getenv("API_KEY")

if __name__ == '__main__':
    # create database object
    db = api.database_api_factory(
        api_key=API_KEY,
        server_ip=SERVER_IP,
        server_port=SERVER_PORT,
    )

    users = db.users.get()

    # === USERS ===
    print("Original:")
    print(db.users.get()['data'][['name', 'email']])

    print("\nNew user:")
    resp = db.users.create(name='Dom RG',
                           email='notarealemail@test.com',
                           short_name='Dom RG',
                           user_score=999,
                           is_rep=True,
                           score_editable=True)
    print(db.users.get()['data'][['name', 'email', 'is_rep']])

    print("\nUpdate 'is_rep':")
    resp = db.users.update(key='notarealemail@test.com', is_rep=False)
    print(db.users.get()['data'][['name', 'email', 'is_rep', 'user_score']])

    print("\nUpdate with invalid key:")
    resp = db.users.update(key='notarealemail@test.com', universial_credit_score=0)
    print(db.users.get()['data'][['name', 'email', 'score_editable', 'user_score']])

    print("\nUpdate 'user_score':")
    resp = db.users.update(key='notarealemail@test.com', user_score=995)
    print(db.users.get()['data'][['name', 'email', 'score_editable', 'user_score']])

    print("\nDelete user:")
    resp = db.users.delete(key='notarealemail@test.com')
    print(db.users.get()['data'][['name', 'email', 'slice_failed_count']])

    print("\nUpdate 'slice_failed_count' by id")
    db.users.update(key=4, slice_failed_count=10)
    print(db.users.get()['data'][['name', 'email', 'slice_failed_count']])
```

## Dependencies
The client has the following dependencies:
- Requests (>=2.28.1)
- Pandas (>=1.5.2)
