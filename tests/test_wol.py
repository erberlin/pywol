import pytest

from pywol.wol import _generate_magic_packet


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
