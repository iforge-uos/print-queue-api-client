import copy
import requests as rq
import time
import logging
import json
import pandas as pd


def log_request_details(func):  # add basic logging to requests
    def wrapper(*args, **kwargs):
        start = time.time()
        resp = func(*args, **kwargs)
        end = time.time()
        if isinstance(resp, rq.Response):
            logging.info(
                f"Request to {resp.url}\n"
                f"\tStatus code {resp.status_code}, Reason: {resp.reason}\n"
                f"\tContent: {resp.headers['Content-Type']}, len: {resp.headers['Content-Length']}\n"
                f"\tTime: {(end - start):3f}s"
            )
        else:
            logging.error("log_request_details used on !Requests.Response()")
        return resp

    return wrapper


def input_to_lower(func):
    def wrapper(*args, **kwargs):
        lower_args = [a.lower() if isinstance(a, str) else a for a in args]
        lower_kwargs = {
            k: (v.lower() if isinstance(v, str) else v) for k, v in kwargs.items()
        }
        return func(*lower_args, **lower_kwargs)

    return wrapper


def interpret_response(
    func,
):  # convert request response (string) to variable (via json.loads)
    """
    iForge Request Response Standards:
    {
      "status": "success"/"error",
      "data": { Success-specific data (eg application) / None or optional error payload },
      "message": { None or optional success message / Error-specific data (eg debug) }
    }

    :return (bool error, str data, str message):
    """

    def wrapper(*args, **kwargs):
        resp = func(*args, **kwargs)
        if isinstance(resp, rq.Response):
            details = json.loads(resp.text)
            error = details["status"] != "success"
            data = details["data"]
            message = details["message"]
            return {"error": error, "data": data, "message": message}
        else:
            err_str = f"Request response is not of the right type, response:\n{resp}"
            logging.error(err_str)
            return {"error": True, "data": None, "message": err_str}

    return wrapper


def result_to_df(func):  # convert returned result to dataframe
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        if result["error"]:
            logging.info(f"Got error, message={result['message']}")
            return None
        else:
            raw_data = copy.deepcopy(result["data"])
            result["data"] = pd.DataFrame(raw_data)
            return result

    return wrapper


class base_table:
    def __init__(self, base_url, header, table_type):
        self.url = base_url + f"/{table_type}"
        self.header = header
        self.table_type = table_type

    # @input_to_lower
    @interpret_response
    @log_request_details
    def _request_action(self, method, action, url_suffix=None, header=None, body=None):
        if not header:
            header = copy.deepcopy(self.header)

        if body is None or type(body) is str:
            data = body
        else:
            data = json.dumps(body)

        if url_suffix is None and method in ["post"]:
            response = rq.request(
                method=method, headers=header, url=f"{self.url}/{action}", data=data
            )
        elif type(url_suffix) is str:  # it's an email
            response = rq.request(
                method=method,
                headers=header,
                url=f"{self.url}/{action}/{url_suffix.lower()}",
                data=data,
            )
        elif type(url_suffix) is int:  # it's an id
            response = rq.request(
                method=method,
                headers=header,
                url=f"{self.url}/{action}/{url_suffix}",
                data=data,
            )
        else:  # it's wrong
            logging.error(
                f"'{url_suffix}' is an invalid unique identifier, cannot {action} {self.table_type}(s)"
            )
            return None
        return response
