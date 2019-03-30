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
    help="IPv4 broadcast address of target subnet.",
)
@click.option("--port", "--p", default=9, show_default=True, help="Target port.")
@click.option("--verbose", "--v", is_flag=True)
def cli(mac_address, ip_address, port, verbose):
    """CLI for the Pywol package.

    Prefer specifying the IPv4 broadcast address of the target host
    subnet over the default '255.255.255.255'.

    """

    if verbose:
        click.echo(f"Waking '{mac_address}' at {ip_address}:{port}...")
    wake(mac_address, ip_address=ip_address, port=port)


if __name__ == "__main__":
    cli()
