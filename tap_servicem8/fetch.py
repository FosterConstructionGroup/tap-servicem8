from datetime import datetime, timezone
import re
import singer
import singer.metrics as metrics
from singer import metadata
from singer.bookmarks import get_bookmark
from tap_servicem8.utility import (
    get_resource,
    transform_record,
    parse_date,
    format_date,
    date_format,
)


def handle_resource(resource, schema, state, mdata):
    bookmark = get_bookmark(state, resource, "since")
    # Current time in local timezone as "aware datetime", per https://stackoverflow.com/a/25887393/7170445
    extraction_time = datetime.now(timezone.utc).astimezone()

    rows = [
        transform_record(row, schema["properties"])
        for row in get_resource(resource, bookmark)
    ]

    if resource == "job_materials":
        rows = handle_job_materials(rows)

    write_many(rows, resource, schema, mdata, extraction_time)
    return write_bookmark(state, resource, extraction_time)


def handle_job_materials(rows):
    date_regex = re.compile(r"(\d{2}\/\d{2}\/\d{4})")
    po_regex = re.compile(r"PO=(\S+)")
    inv_regex = re.compile(r"INV=(\S+)")
    for r in rows:
        d = date_regex.search(r["name"])
        if d is not None:
            r["parsed_date"] = format_date(
                parse_date(d.group(), "%d/%m/%Y"), date_format
            )
        p = po_regex.search(r["name"])
        if p is not None:
            r["purchase_order_reference"] = p.group(1)
        inv = inv_regex.search(r["name"])
        if inv is not None:
            r["invoice_reference"] = inv.group(1)

    return rows


def write_many(rows, resource, schema, mdata, dt):
    with metrics.record_counter(resource) as counter:
        for row in rows:
            write_record(row, resource, schema, mdata, dt)
            counter.increment()


def write_record(row, resource, schema, mdata, dt):
    with singer.Transformer() as transformer:
        rec = transformer.transform(row, schema, metadata=metadata.to_map(mdata))
    singer.write_record(resource, rec, time_extracted=dt)


def write_bookmark(state, resource, dt):
    singer.write_bookmark(state, resource, "since", format_date(dt))
    return state
