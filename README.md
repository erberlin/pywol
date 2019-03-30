# Pywol
>A Wake-on-LAN tool written in Python.

[![MIT license](https://img.shields.io/badge/License-MIT-blue.svg)](https://lbesson.mit-license.org/)
![PyPI](https://img.shields.io/pypi/v/pywol.svg)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pywol.svg)
![PyPI - Wheel](https://img.shields.io/pypi/wheel/pywol.svg)
![CircleCI (all branches)](https://img.shields.io/circleci/project/github/erberlin/pywol.svg)

Pywol allows for starting up [WoL](https://en.wikipedia.org/wiki/Wake-on-LAN)-enabled systems over a network<sup>[1](#f1)</sup>, and can either be used as a CLI tool or imported for use in other Python code.

## Installation

```sh
    $ pip install pywol
```

## Usage examples
As a CLI tool:
```sh
    $ pywol 1A:2B:3C:4D:5E:6F --v
    Waking '1A:2B:3C:4D:5E:6F' at 255.255.255.255:9...
    $
    $ pywol --help
    Usage: pywol [OPTIONS] MAC_ADDRESS

      CLI for the Pywol package.
  
      Prefer specifying the IPv4 broadcast address of the target host subnet
      over the default '255.255.255.255'.

    Options:
      --ip_address, --ip TEXT  IPv4 broadcast address of target subnet.  [default:
                              255.255.255.255]
      --port, --p INTEGER      Target port.  [default: 9]
      --verbose, --v
      --help                   Show this message and exit.
```
Imported for use in other code:
```python
    from pywol import wake
    
    wake("1A2B3C4D5E6F", ip_address="192.168.1.255")
    wake("1A-2B-3C-4D-5E-6F", ip_address="192.168.1.255")
```
## Why create another WoL tool?
I needed one and this was an opportunity to learn some stuff.

## TODO
* Documentation
* Support for multiple target hosts
* Support for loading input from file

## Meta

Erik R Berlin – erberlin.dev@gmail.com

Distributed under the MIT license. See ``LICENSE`` for more information.

[https://github.com/erberlin/pywol](https://github.com/erberlin/pywol)

___
<b id="f1">1</b>. Provided that any routers between the client and target hosts are configured to forward broadcast packets.