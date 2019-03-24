# -*- coding: utf-8 -*-
"""Tests for the pywol.cli module.

copyright: © 2019 by Erik R Berlin.
license: MIT, see LICENSE for more details.

"""

from click.testing import CliRunner

from pywol.cli import cli


def test_cli_defaults():
    """Temporary test to experiment with `CliRunner`."""

    runner = CliRunner()
    result = runner.invoke(cli, ["1A2B3C4D5E6F"])
    assert result.exit_code == 0
    assert result.output == "Waking '1A2B3C4D5E6F' at 255.255.255.255:9 ...\n"


def test_cli_invalid_mac():
    """Temporary test to experiment with `CliRunner`."""

    runner = CliRunner()
    result = runner.invoke(cli, ["1A2B3C4D5E6FF"])
    assert result.exit_code == 0
    assert result.output == (
        "Waking '1A2B3C4D5E6FF' at 255.255.255.255:9 ...\n"
        "Invalid MAC address supplied: '1A2B3C4D5E6FF'.\n"
        "A MAC address should contain 12 hexadecimal digits.\n"
    )
