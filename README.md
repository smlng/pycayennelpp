# PyCayenneLPP

A Cayenne Low Power Payload (CayenneLPP) decoder and encoder for Python.
This is a free open source software project published under the permissive
[MIT License](LICENSE).

Please take note of the [contributing guidelines](CONTRIBUTING.md) and the
[Code of Conduct](CODE_OF_CONDUCT.md).

## Requirements

PyCayenneLPP does not have any external dependencies and only uses builtin
functions and types of Python 3. It requires at least Python in version 3.4.
The PyCayenneLPP package is available via PyPi using `pip`. To install it run:

```
pip3 install pycayennelpp
```

## Usage

Simply add this import to your application to utilise PyCayenneLPP:

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
