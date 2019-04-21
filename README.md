# Pywol
>A Wake-on-LAN tool written in Python.

[![MIT license](https://img.shields.io/badge/License-MIT-blue.svg)](https://lbesson.mit-license.org/)
![PyPI](https://img.shields.io/pypi/v/pywol.svg)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pywol.svg)
![PyPI - Wheel](https://img.shields.io/pypi/wheel/pywol.svg)
![CircleCI branch](https://img.shields.io/circleci/project/github/erberlin/pywol/master.svg)
[![Documentation Status](https://readthedocs.org/projects/pywol/badge/?version=latest)](https://pywol.readthedocs.io/en/latest/)

Pywol allows for starting up [WoL](https://en.wikipedia.org/wiki/Wake-on-LAN)-enabled systems over a network<sup>[1](#f1)</sup>, and can either be used as a CLI tool or imported for use in other Python code.

## Installation

```console
$ pip install pywol
```

## Usage examples
As a CLI tool:
```console
$ pywol 1A2B3C4D5E6F --v
Sent magic packet for '1A2B3C4D5E6F' to 255.255.255.255:9.
$
$ pywol 1A:2B:3C:4D:5E:6F --v --ip 192.168.1.5/24
Sent magic packet for '1A:2B:3C:4D:5E:6F' to 192.168.1.255:9.
$
$ pywol --help
Usage: pywol [OPTIONS] MAC_ADDRESS

  CLI for the Pywol package.

  Prefer to specify the IPv4 broadcast address of the target host's
  subnet over the default '255.255.255.255'.

  To automatically resolve the broadcast address of a subnet,
  specify the target host's IPv4 address along with its netmask. E.g.
  '192.168.1.5/24' or '192.168.1.5/255.255.255.0' --> '192.168.1.255'

Options:
  --ip_address, --ip TEXT  IPv4 broadcast address or host address with
                            netmask.  [default: 255.255.255.255]
  --port, --p INTEGER      Target port.  [default: 9]
  --verbose, --v
  --help                   Show this message and exit.
```
Imported for use in other code:
```pycon
>>> from pywol import wake
>>>
>>> wake("1A2B3C4D5E6F", ip_address="192.168.1.255")
>>> wake("1A-2B-3C-4D-5E-6F", ip_address="192.168.1.5/24", return_dest=True)
('192.168.1.255', '9')
>>>
```

## Documentation
Additional documentation is available at https://pywol.readthedocs.io/en/latest/.

## Development setup
Clone repo:
```console
$ git clone https://github.com/erberlin/pywol.git
$ cd pywol
```
Create and activate virtual environment on OS X & Linux:
```console
$ python3 -m venv venv
$ source venv/bin/activate
```
Create and activate virtual environment on Windows:
```console
> python -m venv venv
> venv\Scripts\activate
```
Install development requirements:
```console
$ pip install -r dev_requirements.txt
```
Run test suite:
```console
$ pytest -v
```

## Why create another WoL tool?
I needed one and this was an opportunity to learn some stuff.

## Meta

Erik R Berlin - erberlin.dev@gmail.com

Distributed under the MIT license. See ``LICENSE`` for more information.

[https://github.com/erberlin/pywol](https://github.com/erberlin/pywol)

___
<b id="f1">1</b>. Provided that any routers between the client and target hosts are configured to forward broadcast packets.