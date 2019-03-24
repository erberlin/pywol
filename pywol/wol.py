# -*- coding: utf-8 -*-
"""
    pywol.wol
    ---------
    This module implements functionality to generate and send Wake-on-LAN magic packets.

    copyright: © 2019 by Erik R Berlin.
    license: MIT, see LICENSE for more details.

"""


def _generate_magic_packet(mac_address):
    """Generate WoL magic packet.

    A  WoL 'magic packet' payload consists of six FF (255 decimal) bytes
    followed by sixteen repetitions of the target's 6-byte MAC address.

    Parameters
    ----------
    mac_address : str
        12-digit hexadecimal MAC address without separators.

    Returns
    -------
    bytes
        102 byte magic packet payload.

    """

    return bytes.fromhex("FF" * 6 + mac_address * 16)
