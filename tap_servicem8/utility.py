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

endpoints = {
    "categories": "category",
    "companies": "company",
    "job_activities": "jobactivity",
    "job_materials": "jobmaterial",
    "jobs": "job",
    "staff": "staff",
    "materials": "material",
    "queue": "queue",
}


def get_resource(resource, start=0):
    if start == None:
        start = 0

    with metrics.http_request_timer(resource) as timer:
        session.headers.update()

        resp = session.request(
            method="get",
            url=f"{baseUrl}/{endpoints[resource]}.json?$filter=edit_date gt '{start}'",
        )
        if resp.status_code == 401:
            raise AuthException(resp.text)
        if resp.status_code == 403:
            raise AuthException(resp.text)
        if resp.status_code == 404:
            raise NotFoundException(resp.text)
        resp.raise_for_status()

        timer.tags[metrics.Tag.http_status_code] = resp.status_code
        return resp.json()


def transform_record(record, properties):
    for key in record:
        if key in properties:
            prop = properties.get(key)
            # Blank dates aren't returned as null
            if (
                prop.get("format") == "date-time"
                and record[key] == "0000-00-00 00:00:00"
            ):
                record[key] = None

            if prop.get("format") == "date" and record[key] == "0000-00-00":
                record[key] = None

            # booleans are sometimes int {1,0}, which Singer transform handles fine
            # but sometimes are string {"1", "0"}, which Singer always transforms to True
            # so always explicitly parse to int first
            if (prop.get("type")[-1]) == "boolean":
                record[key] = bool(int(record[key]))

    return record


date_format = "%Y-%m-%d"
datetime_format = "%Y-%m-%d %H:%M:%S"


def format_date(dt, format=datetime_format):
    return datetime.strftime(dt, format)


def parse_date(dt, format=date_format):
    return datetime.strptime(dt, format)


def try_parse_date(s):
    try:
        return format_date(parse_date(s, date_format), date_format)
    except:
        return None


def get_abs_path(path):
    return os.path.join(os.path.dirname(os.path.realpath(__file__)), path)
