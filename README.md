# PyCayenneLPP

[![GitHub](https://img.shields.io/badge/License-MIT-blue.svg)](https://github.com/smlng/pycayennelpp/blob/master/LICENSE)
[![pip](https://img.shields.io/badge/version-0.4-red.svg)](https://pypi.org/project/pycayennelpp/)
[![Travis-CI](https://travis-ci.com/smlng/pycayennelpp.svg?branch=master)](https://travis-ci.com/smlng/pycayennelpp)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/169fb391fec84d7e83ee69b8dad3cdc3)](https://www.codacy.com/app/smlng/pycayennelpp?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=smlng/pycayennelpp&amp;utm_campaign=Badge_Grade)

A Cayenne Low Power Payload (CayenneLPP) decoder and encoder written in Python.
The project is under active development; releases will be published on the
fly as soon as a certain number of new features and fixes have been made.

## Getting Started

PyCayenneLPP does not have any external dependencies, but only uses builtin
functions and types of Python 3. It requires at least Python in version 3.4.

### Prerequisites

The PyCayenneLPP package is available via PyPi using `pip`. To install it run:

```Shell
pip3 install pycayennelpp
```

### Usage Example

The following it a simple example how to utilise PyCayenneLPP in your own
application:

```Python
from cayennelpp import LppFrame


# create empty frame
frame = LppFrame()
# add some sensor data
frame.add_temperature(0, -1.2)
frame.add_humidity(6, 34.5)
# get byte buffer
buffer = frame.bytes()
```

## Contributing

Contributing to a free open source software project can take place in many
different ways. Feel free to open issues and create pull request to help
improving this project. Pull request have to pass some automatic tests and
checks before being merged into the master branch.

Please take note of the [contributing guidelines](CONTRIBUTING.md) and the
[Code of Conduct](CODE_OF_CONDUCT.md).

## License

This is a free open source software project published under the permissive
[MIT License](LICENSE).
