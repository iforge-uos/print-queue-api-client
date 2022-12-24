from print_queue_api_client.tables.base_table import *


class user_table(base_table):
    def __init__(self, base_url, header):
        super().__init__(base_url=base_url, header=header, table_type="users")

    @result_to_df
    def get(self, key="all"):
        return self._request_action(method="get", action="view", url_suffix=key)

    def create(
        self,
        email,
        name,
        short_name=None,
        user_score=None,
        is_rep=None,
        score_editable=None,
    ):
        # User details construction
        details = {"email": email, "name": name, "short_name": short_name}

        if user_score is not None:
            details["user_score"] = user_score

        if is_rep is not None:
            details["is_rep"] = is_rep

        if score_editable is not None:
            details["score_editable"] = score_editable

        # Request construction
        header = copy.deepcopy(self.header)
        header["Content-Type"] = "application/json"

        return self._request_action(
            method="post", action="add", header=header, body=details
        )

    def update(self, key, **kwargs):
        # User details construction
        new_details = kwargs

        # TODO: some sanity checking of parameters

        # Request construction
        header = copy.deepcopy(self.header)
        header["Content-Type"] = "application/json"

        return self._request_action(
            method="put",
            action="update",
            url_suffix=key,
            header=header,
            body=new_details,
        )

    def delete(self, key=None):
        """
        Getter function for dataframe of user(s)
        :param key: any of: (user ID <int>, user email <str>)
        :return: Request response (converted to dataframe by decorator)
        """
        return self._request_action(method="delete", action="delete", url_suffix=key)
