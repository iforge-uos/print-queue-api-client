from print_queue_api_client.tables.base_table import *


class PrinterTable(base_table):
    def __init__(self, base_url, header):
        super().__init__(base_url=base_url, header=header, table_type="printers")

    @result_to_df
    def get(self, key="all"):
        return self._request_action(method="get", action="view", url_suffix=key)

    def create(self, printer_name, printer_type, ip, api_key, location):
        # User details construction
        details = {
            "printer_name": printer_name,
            "printer_type": printer_type,
            "ip": ip,
            "api_key": api_key,
            "location": location,
        }

        # Request construction
        header = copy.deepcopy(self.header)
        header["Content-Type"] = "application/json"

        return self._request_action(
            method="post", action="add", header=header, body=details
        )

    def delete(self, key="all"):
        return self._request_action(method="delete", action="delete", url_suffix=key)

    def increment(self, key, **kwargs):
        """
        kwargs = {param_key: increment_value, ... }
        """
        header = copy.deepcopy(self.header)
        header["Content-Type"] = "application/json"

        return self._request_action(
            method="put", action="increment", url_suffix=key, header=header, body=kwargs
        )

    def update(self, key, **kwargs):
        """
        kwargs = {param_key: new_value, ... }
        """
        header = copy.deepcopy(self.header)
        header["Content-Type"] = "application/json"

        return self._request_action(
            method="put", action="update", url_suffix=key, header=header, body=kwargs
        )
