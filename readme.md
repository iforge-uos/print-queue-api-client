# iForge Print Queue API Client [![Version](https://badgen.net/pypi/v/print-queue-api-client/)](https://pypi.org/project/print-queue-api-client/)[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)


## About
This is the repository for the iForge Print Queue API Client. This client is used to interact with the iForge Print Queue API. The API is used to manage print jobs, printers and users in the iForge Print Queue.

## Installation
To install the client, run the following command:

```bash
(.venv): pip install print_queue_api_client
```
## Usage
To use the client, import the client and create an instance of the client. The client requires a valid API key to be passed in. The API key can be obtained from the iForge Print Queue API.

```python
import print_queue_api_client as api

client = api.database_api_factory(
    api_key="YOUR_API_KEY",
    server_ip="127.0.0.1",
    server_port="5000",
)

users = client.users.get()

```
## Documentation
TBD.

## Dependencies
The client has the following dependencies:
- Requests (>=2.28.1)
- Pandas (>=1.5.2)
