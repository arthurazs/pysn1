import pytest
from pysn1 import triplet as t


class TestTripletFromBytes:
    def test_from_bytes(self: "TestTripletFromBytes") -> None:
        triplet = t.Triplet.from_bytes(b"\x81\x01\x01")
        assert triplet.tag == 0x81
        assert triplet.length == 1
        assert triplet.value == b"\x01"
        assert len(triplet) == 3

    def test_from_bytes_empty_value(self: "TestTripletFromBytes") -> None:
        triplet = t.Triplet.from_bytes(b"\x81\x00")
        assert triplet.tag == 0x81
        assert triplet.length == 0
        assert triplet.value == b""
        assert len(triplet) == 2

    def test_from_bytes_no_extended_length(self: "TestTripletFromBytes") -> None:
        value = (b"\x00" * 0x7E) + b"\x01"
        triplet = t.Triplet.from_bytes(b"\x81\x7F" + value)
        assert triplet.tag == 0x81
        assert triplet.length == 0x7F
        assert triplet.value == value
        assert len(triplet) == 0x7F + 2

    def test_from_bytes_extended_length_1(self: "TestTripletFromBytes") -> None:
        value = (b"\x00" * 0x7F) + b"\x01"
        triplet = t.Triplet.from_bytes(b"\x81\x81\x80" + value)
        assert triplet.tag == 0x81
        assert triplet.length == 0x80
        assert triplet.value == value
        assert len(triplet) == 0x80 + 3

    def test_from_bytes_extended_length_2(self: "TestTripletFromBytes") -> None:
        value = (b"\x00" * 0xFF) + b"\x01"
        triplet = t.Triplet.from_bytes(b"\x81\x82\x01\x00" + value)
        assert triplet.tag == 0x81
        assert triplet.length == 0xFF + 1
        assert triplet.value == value
        assert len(triplet) == 0xFF + 1 + 4

    def test_from_bytes_bad_length(self: "TestTripletFromBytes") -> None:
        with pytest.raises(t.TripletBadLengthError):
            t.Triplet.from_bytes(b"\x81\x81\x01\x01")

    def test_from_bytes_too_many_bytes(self: "TestTripletFromBytes") -> None:
        with pytest.raises(t.TripletTooManyBytesError):
            t.Triplet.from_bytes(b"\x81\x01\x00\x01")

    def test_from_bytes_missing_bytes_none(self: "TestTripletFromBytes") -> None:
        with pytest.raises(t.TripletMissingBytesError):
            t.Triplet.from_bytes(b"\x81\x01")

    def test_from_bytes_missing_bytes_value(self: "TestTripletFromBytes") -> None:
        with pytest.raises(t.TripletMissingBytesError):
            t.Triplet.from_bytes(b"\x81\x02\x01")

    def test_from_bytes_missing_length(self: "TestTripletFromBytes") -> None:
        with pytest.raises(t.TripletMissingBytesError):
            t.Triplet.from_bytes(b"\x81\x81")
