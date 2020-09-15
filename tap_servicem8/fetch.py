import singer
import singer.metrics as metrics
from singer import metadata
from singer.bookmarks import get_bookmark
from tap_servicem8.utility import get_resource, formatDate


def handle_resource(resource, schema, state, mdata):
    bookmark = get_bookmark(state, resource, "since")
    extraction_time = singer.utils.now()
    rows = get_resource(resource, bookmark)

    write_many(rows, resource, schema, mdata, extraction_time)
    return write_bookmark(state, resource, extraction_time)


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
    singer.write_bookmark(state, resource, "since", formatDate(dt))
    return state
