# -*- coding: utf-8 -*-
"""Tests for the pywol.wol module.

copyright: © 2019 by Erik R Berlin.
license: MIT, see LICENSE for more details.

"""

import socket

import mock
import pytest

from pywol.wol import (
    _clean_mac_address,
    _evaluate_ip_address,
    _generate_magic_packet,
    _send_udp_broadcast,
    _validate_port_number,
    wake,
)


@pytest.fixture()
def sample_data():
    """Test fixture to supply sample mac addres and payload"""

    sample_data = {
        "mac": "1A2B3C4D5E6F",
        "payload": bytes(
            b"\xff\xff\xff\xff\xff\xff"
            b"\x1a+<M^o\x1a+<M^o\x1a+<M^o\x1a+<M^o"
            b"\x1a+<M^o\x1a+<M^o\x1a+<M^o\x1a+<M^o"
            b"\x1a+<M^o\x1a+<M^o\x1a+<M^o\x1a+<M^o"
            b"\x1a+<M^o\x1a+<M^o\x1a+<M^o\x1a+<M^o"
        ),
    }
    return sample_data


def test__generate_magic_packet_type(sample_data):
    """Returned payload is of type bytes."""

    payload = _generate_magic_packet(sample_data["mac"])
    assert isinstance(payload, bytes)


def test__generate_magic_packet_length(sample_data):
    """Returned payload has a length of 102."""

    payload = _generate_magic_packet(sample_data["mac"])
    assert len(payload) == 102


def test__generate_magic_packet_contents(sample_data):
    """Returned payload is equal to expected payload."""

    payload = _generate_magic_packet(sample_data["mac"])
    assert payload == sample_data["payload"]


@pytest.mark.parametrize(
    "valid_input, expected_output",
    [
        ("AA:BB:CC:DD:EE:FF", "AABBCCDDEEFF"),
        ("A1-B2;C3.D4 E5/F6", "A1B2C3D4E5F6"),
        ("123456abcdef", "123456abcdef"),
    ],
)
def test__clean_mac_address_valid(valid_input, expected_output):
    """Valid inputs should be returned without non-hex characters."""

    mac_cleaned = _clean_mac_address(valid_input)
    assert mac_cleaned == expected_output


@pytest.mark.parametrize(
    "invalid_input", ["AA:BB:CC:DD:EE:FFF", "AA:BB:CC:DD:EE:F", "23456abcdef"]
)
def test__clean_mac_address_invalid(invalid_input):
    """Invalid inputs should raise ValueError."""

    with pytest.raises(ValueError):
        _clean_mac_address(invalid_input)


@pytest.mark.parametrize(
    "target_ip, target_port", [("192.168.1.255", 7), ("255.255.255.255", 9)]
)
@mock.patch("socket.socket.sendto", autospec=True)
def test__send_upd_broadcast(mock_socket, sample_data, target_ip, target_port):
    """Test with specified IP address and port."""

    _send_udp_broadcast(sample_data["payload"], ip_address=target_ip, port=target_port)
    socket.socket.sendto.assert_called_with(
        sample_data["payload"], (target_ip, target_port)
    )


@pytest.mark.parametrize(
    "valid_input",
    ["1.1.1.1", "192.168.0.1", "10.3.16.255", "224.0.0.255", "255.255.255.255"],
)
def test__evaluate_ip_address_valid(valid_input):
    """Subnet broadcast address should be returned."""

    valid_ip = _evaluate_ip_address(valid_input)
    assert valid_ip == valid_input


@pytest.mark.parametrize(
    "ip_with_netmask, expected_broadcast_address",
    [
        ("10.3.16.5/8", "10.255.255.255"),
        ("172.16.10.24/12", "172.31.255.255"),
        ("192.168.40.100/16", "192.168.255.255"),
        ("192.168.0.1/24", "192.168.0.255"),
    ],
)
def test__evaluate_ip_address_with_netmask(ip_with_netmask, expected_broadcast_address):
    """Valid inputs should be returned."""

    broadcast_address = _evaluate_ip_address(ip_with_netmask)
    assert broadcast_address == expected_broadcast_address


@pytest.mark.parametrize(
    "invalid_input",
    ["10.3.1234.100", "192.168.0.256", "10..16.255", "224.0.1", "1.2.3.4.5"],
)
def test__evaluate_ip_address_invalid(invalid_input):
    """Invalid inputs should raise ValueError."""

    with pytest.raises(ValueError):
        _evaluate_ip_address(invalid_input)


@pytest.mark.parametrize("valid_input", [0, 7, 9, 65535])
def test__validate_port_number_valid(valid_input):
    """Valid inputs should be returned."""

    valid_port = _validate_port_number(valid_input)
    assert valid_port == valid_input


@pytest.mark.parametrize("invalid_type", [None, "1", "", 1.2])
def test__validate_port_number_invalid_type(invalid_type):
    """Non-integer inputs should raise TypeError."""

    with pytest.raises(TypeError):
        _validate_port_number(invalid_type)


@pytest.mark.parametrize("invalid_port", [-1, 65536])
def test__validate_port_number_invalid_int_value(invalid_port):
    """Integers not in range 0 - 65535 should raise ValueError."""

    with pytest.raises(ValueError):
        _validate_port_number(invalid_port)


def test_wake_defaults(sample_data):
    """Test pywol.wol.wake with defaults."""

    with mock.patch("pywol.wol._send_udp_broadcast", autospec=True) as send_broadcast:
        wake(sample_data["mac"])
        send_broadcast.assert_called_with(sample_data["payload"], "255.255.255.255", 9)


def test_wake_target_ip_port(sample_data):
    """Test pywol.wol.wake with specified target ip address & port."""

    with mock.patch("pywol.wol._send_udp_broadcast", autospec=True) as send_broadcast:
        wake(sample_data["mac"], ip_address="192.168.1.255", port=7)
        send_broadcast.assert_called_with(sample_data["payload"], "192.168.1.255", 7)


def test_wake_ip_with_netmask(sample_data):
    """Test pywol.wol.wake with specified target ip address + netmask & port."""

    with mock.patch("pywol.wol._send_udp_broadcast", autospec=True) as send_broadcast:
        wake(sample_data["mac"], ip_address="192.168.1.123/24", port=7)
        send_broadcast.assert_called_with(sample_data["payload"], "192.168.1.255", 7)


def test_wake_return_target_kwarg(sample_data):
    """Test pywol.wol.wake with return_target kwarg."""

    with mock.patch("pywol.wol._send_udp_broadcast", autospec=True):
        target = wake(
            sample_data["mac"], ip_address="192.168.1.123", port=7, return_target=True
        )
        assert target == "192.168.1.123:7"
