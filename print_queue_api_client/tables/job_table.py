from print_queue_api_client.tables.base_table import *


class job_table(base_table):
    def __init__(self, base_url, header):
        super().__init__(base_url=base_url, header=header, table_type="jobs")

    @result_to_df
    def get(self, key=None):
        return self._request_action(method="get", action="view", url_suffix=key)

    def create(self, **kwargs):

        required_args = ["gcode_slug", "filament_usage", "print_name", "print_time", "printer_type", "project",
                         "user_id"]
        optional_args = ["colour", "date_added", "date_started", "date_ended", "printer", "project_string",
                         "queue_notes", "rep_check", "status", "stl_slug", "upload_notes"]

        # check if all required arguments are provided
        if not all(arg in kwargs for arg in required_args):
            raise ValueError("Missing required argument(s)")

        # create a dictionary with the provided arguments
        details = {arg: kwargs[arg] for arg in kwargs if arg in required_args + optional_args}

        # Request construction
        header = copy.deepcopy(self.header)
        header["Content-Type"] = "application/json"

        return self._request_action(
            method="post", action="add", header=header, body=details
        )

    def review(self, job_id):
        """
        Place {job_id} under-review
        :param int job_id: job ID
        :return:
        """
        return self._request_action(method="put", action="review", url_suffix=job_id)

    def queue(self, job_id):
        """
        Queue {job_id}
        :param int job_id: job ID
        :return:
        """
        return self._request_action(method="put", action="queue", url_suffix=job_id)

    def reject(self, job_id):
        """
        Reject {job_id}
        :param int job_id: job ID
        :return:
        """
        return self._request_action(method="put", action="reject", url_suffix=job_id)

    def complete(self, job_id):
        """
        Complete {job_id}
        :param int job_id: job ID
        :return:
        """
        return self._request_action(method="put", action="complete", url_suffix=job_id)

    def fail(self, job_id, requeue=False):
        """
        Complete {job_id}
        :param int job_id: job ID
        :param bool requeue: requeue print or not
        :return:
        """
        url_suffix = f"{job_id}"
        if requeue is True:
            url_suffix += "?requeue=yes"
        return self._request_action(method="put", action="fail", url_suffix=url_suffix)

    def start(self, job_id, printer_id, colour="auto-print"):
        details = {"printer": printer_id, "colour": colour}

        # Request construction
        header = copy.deepcopy(self.header)
        header["Content-Type"] = "application/json"

        return self._request_action(
            method="put", action="start", url_suffix=job_id, header=header, body=details
        )

    def delete(self, key=None):
        """
        Getter function for dataframe of user(s)
        :param key: job ID <int>
        :return: Request response (converted to dataframe by decorator)
        """
        return self._request_action(method="delete", action="delete", url_suffix=key)
