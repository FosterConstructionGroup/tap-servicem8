import os
import requests
import singer.metrics as metrics
from datetime import datetime


session = requests.Session()


class AuthException(Exception):
    pass


class NotFoundException(Exception):
    pass


# constants
baseUrl = "https://api.servicem8.com/api_1.0"


def get_resource(source, resource, start=0):
    with metrics.http_request_timer(source) as timer:
        session.headers.update()
        resp = session.request(
            method="get",
            url="{}{}?$filter=edit_date gt '{}'".format(baseUrl, resource, start),
        )
        if resp.status_code == 401:
            raise AuthException(resp.text)
        if resp.status_code == 403:
            raise AuthException(resp.text)
        if resp.status_code == 404:
            raise NotFoundException(resp.text)

        timer.tags[metrics.Tag.http_status_code] = resp.status_code
        return resp


def formatDate(dt):
    return datetime.strftime(dt, "%Y-%m-%d %H:%M:%S")


def get_abs_path(path):
    return os.path.join(os.path.dirname(os.path.realpath(__file__)), path)
