# -*- coding: utf-8 -*-
"""Tests for the pywol.cli module.

copyright: © 2019 by Erik R Berlin.
license: MIT, see LICENSE for more details.

"""

from click.testing import CliRunner

from pywol.cli import cli


def test_cli_defaults():
    """Invoke with only MAC address."""

    runner = CliRunner()
    result = runner.invoke(cli, ["1A2B3C4D5E6F"])
    assert result.exit_code == 0


def test_cli_defaults_verbose():
    """Invoke with MAC address and --v flag."""

    runner = CliRunner()
    result = runner.invoke(cli, ["1A2B3C4D5E6F", "--v"])
    assert result.exit_code == 0
    assert result.output == "Waking '1A2B3C4D5E6F' at 255.255.255.255:9...\n"


def test_cli_no_args():
    """Invoke with no arguments."""

    runner = CliRunner()
    result = runner.invoke(cli)
    assert result.exit_code == 2


def test_cli_invalid_mac():
    """Invoke with invalid MAC address."""

    runner = CliRunner()
    result = runner.invoke(cli, ["1A2B3C4D5E6FF"])
    assert result.output == "[Error] Invalid MAC address: 1A2B3C4D5E6FF\n"


def test_cli_invalid_ip():
    """Invoke with invalid IP address."""

    runner = CliRunner()
    result = runner.invoke(cli, ["1A2B3C4D5E6F", "--ip", "192.168.1.257"])
    assert result.output == "[Error] Invalid IP address: 192.168.1.257\n"


def test_cli_invalid_integer_port():
    """Invoke with invalid port number."""

    runner = CliRunner()
    result = runner.invoke(cli, ["1A2B3C4D5E6F", "--p", "65536"])
    assert result.output == "[Error] Invalid port: 65536\n"


def test_cli_non_integer_port():
    """Invoke with non-integer port value."""

    runner = CliRunner()
    result = runner.invoke(cli, ["1A2B3C4D5E6F", "--p", "a"])
    assert result.exit_code == 2
