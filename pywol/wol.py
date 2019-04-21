# -*- coding: utf-8 -*-
"""
pywol.wol
---------
This module implements functionality to generate and send Wake-on-LAN magic packets.

copyright: © 2019 by Erik R Berlin.
license: MIT, see LICENSE for more details.

"""

import ipaddress
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
        If `mac_address_supplied` does not contain exactly 12 hexadecimal
        characters.

    """

    mac_address_cleaned = NON_HEX_CHARS.sub("", mac_address_supplied)
    if MAC_PATTERN.fullmatch(mac_address_cleaned):
        return mac_address_cleaned
    else:
        raise ValueError(f"[Error] Invalid MAC address: {mac_address_supplied}")


def _evaluate_ip_address(ip_address):
    """Evaluate supplied IPv4 address.

    Returns the supplied IPv4 address if valid and specified without a
    netmask, or returns the subnet broadcast address if the supplied
    IPV4 address is specified with a netmask such as '192.168.1.5/24' or
    '192.168.1.5/255.255.255.0'.

    Parameters
    ----------
    ip_address : str
        Supplied IP address.

    Returns
    -------
    str
        Valid IPv4 address.

    Raises
    ------
    ValueError
        If `ip_address` does not contain a valid IPv4 address.

    """

    ip = ip_address.strip()
    try:
        ip = str(ipaddress.IPv4Address(ip))
    except ipaddress.AddressValueError:
        try:
            ip = str(ipaddress.IPv4Network(ip, strict=False).broadcast_address)
        except Exception as e:
            raise ValueError(f"[Error] Invalid IP address: {ip_address}") from e
    return ip


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


def _send_udp_broadcast(payload, ip_address, port):
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


def _validate_port_number(port_number):
    """Validate port number.

    Parameters
    ----------
    port_number : int
        Supplied port number.

    Returns
    -------
    int
        Valid port number.

    Raises
    ------
    TypeError
        If `port_number` is not of type int.
    ValueError
        If `port_number` is not in range 0 - 65535.

    """

    if not isinstance(port_number, int):
        raise TypeError(f"[Error] Port number must be of type int.")
    elif 0 <= port_number <= 65535:
        return port_number
    else:
        raise ValueError(f"[Error] Invalid port number: {port_number}")


def wake(mac_address, *, ip_address="255.255.255.255", port=9, return_dest=False):
    """Generate and send WoL magic packet.

    Prefer to specify the IPv4 broadcast address of the target host's
    subnet over the default '255.255.255.255'.

    To automatically resolve the broadcast address of a subnet,
    specify the target host's IPv4 address along with its netmask. E.g.
    '192.168.1.5/24' or '192.168.1.5/255.255.255.0' --> '192.168.1.255'

    Parameters
    ----------
    mac_address : str
        Target MAC address.
    ip_address : str, optional
        Target IPv4 address. (default is '255.255.255.255').
    port : int, optional
        Target port. (default is 9).
    return_dest : bool, optional
        Flag to return package destination ip & port on success.
        (default is False).

    Returns
    -------
    tuple(str, str)
        Returns destination IP & port of successfully sent package
        if `return_dest` is True.

    """

    try:
        mac_cleaned = _clean_mac_address(mac_address)
        valid_ip_address = _evaluate_ip_address(ip_address)
        valid_port = _validate_port_number(port)
    except ValueError as e:
        print(e)
    except TypeError as e:
        print(e)
    else:
        payload = _generate_magic_packet(mac_cleaned)
        try:
            _send_udp_broadcast(payload, valid_ip_address, valid_port)
        except OSError:
            print(f"[Error] Cannot send broadcast to IP address: {valid_ip_address}")
        else:
            if return_dest is True:
                return (valid_ip_address, str(valid_port))
