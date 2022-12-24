import logging

from print_queue_api_client.tables.job_table import job_table
from print_queue_api_client.tables.printer_table import PrinterTable
from print_queue_api_client.tables.user_table import user_table

logging.basicConfig()
logging.getLogger().setLevel(logging.INFO)


class database_api:
    def __init__(self, server_ip, server_port, api_key):
        API_PREFIX = "/api/v1"
        self.base_url = f"http://{server_ip}:{server_port}{API_PREFIX}"
        self.header = {"x-api-key": f"{api_key}"}

        self.users = user_table(self.base_url, self.header)
        self.printers = PrinterTable(self.base_url, self.header)
        self.jobs = job_table(self.base_url, self.header)

    def __repr__(self):
        return f"database_api({self.base_url}, {self.header})"
