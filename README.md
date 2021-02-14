# tap-servicem8

This is a [Singer](https://singer.io) tap that produces JSON-formatted
data from the ServiceM8 API following the [Singer
spec](https://github.com/singer-io/getting-started/blob/master/SPEC.md).

This tap:

- Pulls raw data from the [ServiceM8 API](https://developer.servicem8.com/docs)
- Extracts the following resources from ServiceM8:
  - Jobs
  - Clients
  - Categories
- Outputs the schema for each resource
- Incrementally pulls data based on the input state

## Quick start

1. Install

   We recommend using a virtualenv:

   ```bash
   > virtualenv -p python3 venv
   > source venv/bin/activate
   > pip install -e .
   ```

2. Create the config file

   Create a JSON file called `config.json` containing your username and password.

   ```json
   { "username": "your_username", "password": "your_password" }
   ```

3. Run the tap in discovery mode to get properties.json file

   ```bash
   tap-servicem8 --config config.json --discover > properties.json
   ```

4. In the properties.json file, select the streams to sync

   Each stream in the properties.json file has a "schema" entry. To select a stream to sync, add `"selected": true` to that stream's "schema" entry. For example, to sync the pull_requests stream:

   ```
   ...
   "tap_stream_id": "sites",
   "schema": {
     "selected": true,
     "properties": {
   ...
   ```

5. Run the application

   `tap-servicem8` can be run with:

   ```bash
   tap-servicem8 --config config.json --properties properties.json
   ```
