# -*- coding: utf-8 -*-
"""
    pywol.wol
    ---------
    This module implements functionality to generate and send Wake-on-LAN magic packets.

    copyright: © 2019 by Erik R Berlin.
    license: MIT, see LICENSE for more details.

"""

import re

NON_HEX_CHARS = re.compile(r"[^a-f0-9]", re.IGNORECASE)
MAC_PATTERN = re.compile(r"^[a-f0-9]{12}$", re.IGNORECASE)


def _clean_mac_address(mac_address_supplied):
    """Clean and validate MAC address.

    Removes all non-hexadecimal characters from `mac_address_supplied`
    and returns the result if it's valid.

    Parameters
    ----------
    mac_address_supplied : str
        Supplied MAC address.

    Returns
    -------
    str
        12-digit hexadecimal MAC address without any separators.

    Raises
    ------
    ValueError
        If `mac_address_cleaned` does not contain exactly 12 hexadecimal
        characters.

    """

    mac_address_cleaned = NON_HEX_CHARS.sub("", mac_address_supplied).lower()
    if MAC_PATTERN.fullmatch(mac_address_cleaned):
        return mac_address_cleaned
    else:
        raise ValueError(
            f"Invalid MAC address supplied: {mac_address_supplied}."
            "A MAC address should contain 12 hexadecimal digits."
        )


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
        102-byte magic packet payload.

    """

    return bytes.fromhex("FF" * 6 + mac_address * 16)
