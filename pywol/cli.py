# -*- coding: utf-8 -*-
"""
pywol.cli
---------
This module implements a simple CLI for the pywol package.

copyright: © 2019 by Erik R Berlin.
license: MIT, see LICENSE for more details.

"""

import click

from .wol import wake


@click.command()
@click.argument("mac_address")
@click.option(
    "--ip_address",
    "--ip",
    default="255.255.255.255",
    show_default=True,
    help="IPv4 broadcast address or host address with netmask.",
)
@click.option("--port", "--p", default=9, show_default=True, help="Target port.")
@click.option("--verbose", "--v", is_flag=True)
def cli(mac_address, ip_address, port, verbose):
    """CLI for the Pywol package.

    Prefer to specify the IPv4 broadcast address of the target host's
    subnet over the default '255.255.255.255'.

    To automatically resolve the broadcast address of a subnet,
    specify the target host's IPv4 address along with its netmask. E.g.
    '192.168.1.5/24' or '192.168.1.5/255.255.255.0' --> '192.168.1.255'

    """

    dest = wake(mac_address, ip_address=ip_address, port=port, return_dest=True)
    if verbose and dest:
        click.echo(f"Sent magic packet for '{mac_address}' to {dest[0]}:{dest[1]}.")


if __name__ == "__main__":
    cli()
