import pytest

from pywol.wol import _generate_magic_packet, _clean_mac_address


@pytest.fixture()
def sample_data():
    """Test fixture to supply sample mac addres and payload"""

    sample_data = {
        "mac": "1A2B3C4D5E6F",
        "expected_payload": bytes(
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
    assert payload == sample_data["expected_payload"]


@pytest.mark.parametrize(
    "valid_input, expected_output",
    [
        ("AA:BB:CC:DD:EE:FF", "aabbccddeeff"),
        ("A1-B2;C3.D4 E5/F6", "a1b2c3d4e5f6"),
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
