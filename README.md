# Rackspace CLI

Command line client for interacting with various Rackspace Cloud APIs.

## Installation

Command line client is available on PyPi and can be installed using pip:

```bash
pip install -r raxcli
```

## Usage

```bash
raxcli <service> <resource> <action> [options]
```

For example:

```bash
raxcli registry services list
```

### Custom Output Formatter

To specify a custom formatter, use `-f` option. For example:

`raxcli registry services list -f json`

#### Available Formatters

* table
* csv
* json
* yaml
* html

## Development

### Testing and Lint

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
