import logging
import pandas as pd
import os
import dotenv

from JobTable import JobTable
from PrinterTable import PrinterTable
from UserTable import UserTable

dotenv.load_dotenv("./.env")


logging.basicConfig()
logging.getLogger().setLevel(logging.INFO)

SERVER_IP = os.getenv("SERVER_IP")
SERVER_PORT = os.getenv("SERVER_PORT")
API_KEY = os.getenv("API_KEY")


class DatabaseApi:
    def __init__(self, server_ip, server_port, api_key):
        API_PREFIX = '/api/v1'
        self.base_url = f'http://{server_ip}:{server_port}{API_PREFIX}'
        self.header = {'x-api-key': f'{api_key}'}

        self.users = UserTable(self.base_url, self.header)
        self.printers = PrinterTable(self.base_url, self.header)
        self.jobs = JobTable(self.base_url, self.header)


if __name__ == '__main__':
    db = DatabaseApi(SERVER_IP, SERVER_PORT, API_KEY)
    # === USERS ===
    # result = db.users.get()
    # print(result['email'])
    # success, resp = db.users.create(name='Dominic Rugg-Gunn', email='notarealemail@test.com', short_name='Dom RG',
    #                                 user_score=999, is_rep=True, score_editable=False)
    # print(db.users.get().head())
    # success, resp = db.users.update(key='notarealemail@test.com', is_rep=False)
    # print(db.users.get().head())
    # success, resp = db.users.update(key='notarealemail@test.com', universial_credit_score=0)
    # print(db.users.get().head())
    # success, resp = db.users.delete(key='notarealemail@test.com')
    # print(db.users.get().head())
    # db.users.update(4, slice_failed_count=0)

    # === JOBS ===
    params = {
        "user_id": 4,
        "print_name": "test",
        "gcode_slug": "cagsad7bnja",
        "upload_notes": "SYSTEM TEST DO NOT PRINT",
        "printer_type": "prusa",
        "project": "personal",
        "print_time": 69,
        "filament_usage": 420
    }
    db.jobs.create(**params)
    df = db.jobs.get("under_review")['data']
    df.update(db.jobs.get("queued")['data'])
    # print(review_df.head())
    ids = df['id']
    for id in ids:
        db.jobs.queue(int(id))
    # print(db.jobs.queue(11))
    # print(db.jobs.reject(12))