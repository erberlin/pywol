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
    "--ip",
    "--ip_address",
    default="255.255.255.255",
    show_default=True,
    help="IPv4 broadcast address of target subnet.",
)
@click.option("--port", default=9, show_default=True, help="Target port.")
def cli(mac_address, ip, port):
    """CLI for the pywol package.

    Prefer specifying the broadcast IPv4 address of the target host
    subnet over the default '255.255.255.255'.

    """

    click.echo(f"Waking '{mac_address}' at {ip}:{port}...")
    wake(mac_address, ip_address=ip, port=port)


if __name__ == "__main__":
    cli()
