# Pywol
>A Wake-on-LAN tool written in Python.

[![MIT license](https://img.shields.io/badge/License-MIT-blue.svg)](https://lbesson.mit-license.org/)

Pywol allows for starting up WoL-enabled systems over a network[^1], and can either be used as a CLI tool or imported into other Python code.

## Installation

```sh
    $ pip install pywol
```

## Usage examples
As a CLI tool:
```sh
    $ pywol 1A:2B:3C:4D:5E:6F --ip 192.168.1.255
    Waking '1A:2B:3C:4D:5E:6F' at 192.168.1.255:9...
    $
    $ pywol --help
    Usage: pywol [OPTIONS] MAC_ADDRESS

    CLI for the pywol package.

    Prefer specifying the broadcast IPv4 address of the target host subnet
    over the default '255.255.255.255'.

    Options:
    --ip, --ip_address TEXT  IPv4 broadcast address of target subnet.  [default:
                            255.255.255.255]
    --port INTEGER           Target port.  [default: 9]
    --help                   Show this message and exit.
```
Imported for use in other code:
```python
    from pywol import wake
    wake("1A:2B:3C:4D:5E:6F", ip_address="192.168.1.255")
```
## Why create another WoL tool?
I needed one and this was an opportunity to learn some stuff.

## TODO
* Logging
* Support for multiple target hosts
* Support for loading input from files
* Documentation

## Meta

Erik R Berlin – erberlin.dev@gmail.com

Distributed under the MIT license. See ``LICENSE`` for more information.

[https://github.com/erberlin/pywol](https://github.com/erberlin/pywol)
---
[^1]: Provided that any routers between the client and target hosts are configured to forward broadcast packets.