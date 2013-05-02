# Rackspace CLI

Command line client for interacting with various Rackspace Cloud APIs.

## Testing and Lint

Running tests

```bash
python setup.py test
```

Running lint

```bash
python setup.py flake8
```

## Goals / Brain dump

* Common command line client for all the Rackspace Cloud APIs
* Supports user and machine friendly input and output formats
* Default to user friendly output format
* Multiple output formats (table, json, csv)
* Command structure which makes sense - raxcli <service> <resource> <action>
* Supported Python version - 2.6, 2.7, PyPy
* Autocomplete
* REPL for every api
* Friendly debug output when using --debug
* Print CURL request actions when using --debug
* Single, undefined configuration file (~/.raxrc)

## License

Library is distributed under the [Apache 2.0 license](http://www.apache.org/licenses/LICENSE-2.0.html).
