# PyCayenneLPP

[![Travis-CI](https://travis-ci.com/smlng/pycayennelpp.svg?branch=master)](https://travis-ci.com/smlng/pycayennelpp)
[![Codacy Badge](https://app.codacy.com/project/badge/Grade/a47d55068ce348c2a83497d2ab5f07bf)](https://www.codacy.com/gh/smlng/pycayennelpp/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=smlng/pycayennelpp&amp;utm_campaign=Badge_Grade)
[![Codacy Badge](https://app.codacy.com/project/badge/Coverage/a47d55068ce348c2a83497d2ab5f07bf)](https://www.codacy.com/gh/smlng/pycayennelpp/dashboard?utm_source=github.com&utm_medium=referral&utm_content=smlng/pycayennelpp&utm_campaign=Badge_Coverage)
[![PyPi](https://badge.fury.io/py/pycayennelpp.svg)](https://badge.fury.io/py/pycayennelpp)
[![GitHub](https://img.shields.io/badge/License-MIT-blue.svg)](https://github.com/smlng/pycayennelpp/blob/master/LICENSE)

A Cayenne Low Power Payload (CayenneLPP) decoder and encoder written in Python.

PyCayenneLPP offers a concise interface with proper encoding and decoding
functionality for the CayenneLPP format suporting many sensor types. Further, 
the project aims for overall high code quality and good test coverage.

See also [myDevicesIoT/CayenneLPP](https://github.com/myDevicesIoT/CayenneLPP)
for more information on the format and a reference implementation in C++.

The project is under active development. Releases will be published on the
fly as soon as a certain number of new features and fixes have been made.

## Supported Data Types

The following table lists the currently supported data types with the LPP code
(which equals IPSO code - 3200), data size in bytes, and data dimensions.

| Type Name      | LPP | Size | Dim |
|----------------|-----|------|-----|
| Digital Input  |   0 |    1 |   1 |
| Digital Output |   1 |    1 |   1 |
| Analog Input   |   2 |    2 |   1 |
| Analog Output  |   3 |    2 |   1 |
| Generic        | 100 |    4 |   1 |
| Illuminance    | 101 |    2 |   1 |
| Presence       | 102 |    1 |   1 |
| Temperature    | 103 |    2 |   1 |
| Humidity       | 104 |    1 |   1 |
| Accelerometer  | 113 |    6 |   3 |
| Barometer      | 115 |    2 |   1 |
| Voltage        | 116 |    2 |   1 |
| Load           | 122 |    3 |   1 |
| Unix Time      | 133 |    4 |   1 |
| Gyrometer      | 134 |    6 |   3 |
| GPS Location   | 136 |    9 |   3 |

## Getting Started

PyCayenneLPP does not have any external dependencies and only uses builtin
functions and types of Python 3. It is compatible with all the latest and 
officially supported Python versions 3.6 and above, though even Python 3.4 
will do.

Since PyCayenneLPP 1.2.0 MicroPython is officially supported, and published 
as a separate package under `micropython-pycayennelpp`.

### Python 3 Prerequisites

The PyCayenneLPP package is available via PyPi using `pip`. To install it run:

```Shell
pip3 install pycayennelpp
```

### MicroPython Prerequisites

Using MicroPythons `upip` module PyCayenneLPP can be installed as follows
within MicroPython:

```Python
import upip
upip.install("micropython-pycayennelpp")
```

Or alternatively run with in a shell:

```Shell
micropython -m upip install micropython-pycayennelpp
```

### Usage Examples

The following show how to utilise PyCayenneLPP in your own application
to encode and decode data into and from CayenneLPP. The code snippets
work with standard Python 3 as well as MicroPython, assuming you have
installed the PyCayenneLPP package as shown above.

***Encoding***

```Python
from cayennelpp import LppFrame


# create empty frame
frame = LppFrame()
# add some sensor data
frame.add_temperature(0, -1.2)
frame.add_humidity(6, 34.5)
# get byte buffer in CayenneLPP format
buffer = bytes(frame)
```

***Decoding***

```Python
from cayennelpp import LppFrame


# byte buffer in CayenneLPP format with 1 data item
# i.e. on channel 1, with a temperature of 25.5C
buffer = bytearray([0x01, 0x67, 0x00, 0xff])
# create frame from bytes
frame = LppFrame().from_bytes(buffer)
# print the frame and its data
print(frame)
```

## Contributing

Contributing to a free open source software project can take place in many
different ways. Feel free to open issues and create pull requests to help
improving this project. Each pull request has to pass some automatic tests and
checks run by Travis-CI before being merged into the master branch.

Please take note of the [contributing guidelines](CONTRIBUTING.md) and the
[Code of Conduct](CODE_OF_CONDUCT.md).

## License

This is a free open source software project published under the [MIT License](LICENSE).
