# -*- coding: utf-8 -*-
"""
pywol.wol
---------
This module implements functionality to generate and send Wake-on-LAN magic packets.

copyright: © 2019 by Erik R Berlin.
license: MIT, see LICENSE for more details.

"""

import re
import socket

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
        raise ValueError(f"[Error] Invalid MAC address: {mac_address_supplied}")


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


def _send_upd_broadcast(payload, ip_address, port):
    """Send data as UDP broadcast message.

    Parameters
    ----------
    payload : bytes
        Should be 102-byte magic packet payload.
    ip_address : str
        Target IP address.
    port : int
        Target port.

    """

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        sock.sendto(payload, (ip_address, port))


def wake(mac_address, *, ip_address="255.255.255.255", port=9):
    """Generate and send WoL magic packet.

    Prefer specifying the broadcast IPv4 address of the target host
    subnet over the default universal '255.255.255.255'.

    Parameters
    ----------
    mac_address : str
        Supplied MAC address.
    ip_address : str, optional
        Target IP address. (default is '255.255.255.255').
    port : int, optional
        Target port. (default is 9).

    """

    try:
        mac_cleaned = _clean_mac_address(mac_address)
    except ValueError as e:
        print(e)
    else:
        payload = _generate_magic_packet(mac_cleaned)
        try:
            _send_upd_broadcast(payload, ip_address, port)
        except OSError:
            print(f"[Error] Invalid IP address: {ip_address}")
        except OverflowError:
            print(f"[Error] Invalid port: {port}")
