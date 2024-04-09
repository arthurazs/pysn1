import pytest

from pysn1 import triplet as t

DEFAULT_TAG = 0x81


class TestTripletBuild:
    def test_correct_creation(self: "TestTripletBuild") -> None:
        value = b"pysn1"
        triplet = t.Triplet.build(tag=DEFAULT_TAG, value=value)
        assert triplet.tag == DEFAULT_TAG
        assert triplet.length == len(value)
        assert triplet.value == value
        assert len(triplet) == len(value) + 2
        assert bytes(triplet) == b"\x81\x05pysn1"

class TestTripletFromBytes:
    def test_from_bytes(self: "TestTripletFromBytes") -> None:
        bytestring = b"\x81\x01\x01"
        triplet = t.Triplet.from_bytes(bytestring)
        assert triplet.tag == DEFAULT_TAG
        assert triplet.length == 1
        assert triplet.value == b"\x01"
        assert len(triplet) == len(bytestring)
        assert bytes(triplet) == bytestring

    def test_from_bytes_empty_value(self: "TestTripletFromBytes") -> None:
        bytestring = b"\x81\x00"
        triplet = t.Triplet.from_bytes(bytestring)
        assert triplet.tag == DEFAULT_TAG
        assert triplet.length == 0
        assert triplet.value == b""
        assert len(triplet) == len(bytestring)
        assert bytes(triplet) == bytestring

    def test_from_bytes_no_extended_length(self: "TestTripletFromBytes") -> None:
        length = 0x7F
        value = (b"\x00" * (length - 1)) + b"\x01"
        bytestring = b"\x81\x7F" + value
        triplet = t.Triplet.from_bytes(bytestring)
        assert triplet.tag == DEFAULT_TAG
        assert triplet.length == length
        assert triplet.value == value
        assert len(triplet) == len(bytestring)
        assert bytes(triplet) == bytestring

    def test_from_bytes_extended_length_1(self: "TestTripletFromBytes") -> None:
        length = 0x80
        value = (b"\x00" * (length - 1)) + b"\x01"
        bytestring = b"\x81\x81\x80" + value
        triplet = t.Triplet.from_bytes(bytestring)
        assert triplet.tag == DEFAULT_TAG
        assert triplet.length == length
        assert triplet.value == value
        assert len(triplet) == len(bytestring)
        assert bytes(triplet) == bytestring

    def test_from_bytes_extended_length_2(self: "TestTripletFromBytes") -> None:
        length = 0x100
        value = (b"\x00" * (length - 1)) + b"\x01"
        bytestring = b"\x81\x82\x01\x00" + value
        triplet = t.Triplet.from_bytes(bytestring)
        assert triplet.tag == DEFAULT_TAG
        assert triplet.length == length
        assert triplet.value == value
        assert len(triplet) == len(bytestring)
        assert bytes(triplet) == bytestring

    def test_from_bytes_too_many_bytes(self: "TestTripletFromBytes") -> None:
        value = b"\x00"
        bytestring = b"\x81\x01" + value + b"\x01"
        triplet = t.Triplet.from_bytes(bytestring)
        assert triplet.tag == DEFAULT_TAG
        assert triplet.length == 1
        assert triplet.value == value
        assert len(triplet) == len(bytestring)
        assert bytes(triplet) == bytestring[:-1]

    @pytest.mark.skip(reason="too slow")
    def test_from_bytes_too_big(self: "TestTripletFromBytes") -> None:
        value = (b"\x00" * t.EXTENDED_LENGTH_4) + b"\x01"
        bytestring = b"\x81\x85\x01\x00\x00\x00\x00" + value
        with pytest.raises(t.TripletLengthTooBigError) as exc_info:
            t.Triplet.from_bytes(bytestring)
        assert exc_info.match("Triplet with extended length > 4 not implemented")

    def test_from_bytes_bad_length(self: "TestTripletFromBytes") -> None:
        with pytest.raises(t.TripletBadLengthError) as exc_info:
            t.Triplet.from_bytes(b"\x81\x81\x01\x01")
        assert exc_info.match(r"Triplet contains extended length, but extended length is less than 128 \(0x80\)")

    def test_from_bytes_missing_bytes_none(self: "TestTripletFromBytes") -> None:
        with pytest.raises(t.TripletMissingBytesError) as exc_info:
            t.Triplet.from_bytes(b"\x81\x01")
        assert exc_info.match("Triplet length is 1, but value contains only 0 bytes")

    def test_from_bytes_missing_bytes_value(self: "TestTripletFromBytes") -> None:
        with pytest.raises(t.TripletMissingBytesError) as exc_info:
            t.Triplet.from_bytes(b"\x81\x02\x01")
        assert exc_info.match("Triplet length is 2, but value contains only 1 bytes")

    def test_from_bytes_missing_length(self: "TestTripletFromBytes") -> None:
        with pytest.raises(t.TripletMissingBytesError) as exc_info:
            t.Triplet.from_bytes(b"\x81\x81")
        assert exc_info.match("Triplet extended length is missing bytes")


class TestTriplet:
    def test_from_bytes(self: "TestTriplet") -> None:
        bytestring = b"\x81\x01\x01"
        triplet = t.Triplet(tag=DEFAULT_TAG, length=1, value=b"\x01")
        assert triplet.tag == DEFAULT_TAG
        assert triplet.length == 1
        assert triplet.value == b"\x01"
        assert len(triplet) == len(bytestring)
        assert bytes(triplet) == bytestring

    def test_from_bytes_empty_value(self: "TestTriplet") -> None:
        bytestring = b"\x81\x00"
        triplet = t.Triplet(tag=DEFAULT_TAG, length=0)
        assert triplet.tag == DEFAULT_TAG
        assert triplet.length == 0
        assert triplet.value == b""
        assert len(triplet) == len(bytestring)
        assert bytes(triplet) == bytestring

    def test_from_bytes_no_extended_length(self: "TestTriplet") -> None:
        length = 0x7F
        value = (b"\x00" * (length - 1)) + b"\x01"
        bytestring = b"\x81\x7F" + value
        triplet = t.Triplet(tag=DEFAULT_TAG, length=length, value=value)
        assert triplet.tag == DEFAULT_TAG
        assert triplet.length == length
        assert triplet.value == value
        assert len(triplet) == len(bytestring)
        assert bytes(triplet) == bytestring

    def test_from_bytes_extended_length_1(self: "TestTriplet") -> None:
        length = 0x80
        value = (b"\x00" * (length - 1)) + b"\x01"
        bytestring = b"\x81\x81\x80" + value
        triplet = t.Triplet(tag=DEFAULT_TAG, length=length, value=value)
        assert triplet.tag == DEFAULT_TAG
        assert triplet.length == length
        assert triplet.value == value
        assert len(triplet) == len(bytestring)
        assert bytes(triplet) == bytestring

    def test_from_bytes_extended_length_2(self: "TestTriplet") -> None:
        length = 0x100
        value = (b"\x00" * (length - 1)) + b"\x01"
        bytestring = b"\x81\x82\x01\x00" + value
        triplet = t.Triplet(tag=DEFAULT_TAG, length=length, value=value)
        assert triplet.tag == DEFAULT_TAG
        assert triplet.length == length
        assert triplet.value == value
        assert len(triplet) == len(bytestring)
        assert bytes(triplet) == bytestring

    @pytest.mark.skip(reason="too slow")
    def test_from_bytes_too_big_correct_value(self: "TestTriplet") -> None:
        value = (b"\x00" * t.EXTENDED_LENGTH_4) + b"\x01"
        with pytest.raises(t.TripletLengthTooBigError) as exc_info:
            t.Triplet(tag=DEFAULT_TAG, length=0xFFFFFFFF + 1, value=value)
        assert exc_info.match("Triplet with extended length > 4 not implemented")

    def test_from_bytes_too_big_missing_value(self: "TestTriplet") -> None:
        with pytest.raises(t.TripletLengthTooBigError) as exc_info:
            t.Triplet(tag=DEFAULT_TAG, length=0xFFFFFFFF + 1, value=b"")
        assert exc_info.match("Triplet with extended length > 4 not implemented")

    def test_from_bytes_too_many_bytes(self: "TestTriplet") -> None:
        with pytest.raises(t.TripletTooManyBytesError) as exc_info:
            t.Triplet(tag=DEFAULT_TAG, length=1, value=b"\x00\x01")
        assert exc_info.match("Triplet length is 1, but value contains 2 bytes")

    def test_from_bytes_missing_bytes_none(self: "TestTriplet") -> None:
        with pytest.raises(t.TripletMissingBytesError) as exc_info:
            t.Triplet(tag=DEFAULT_TAG, length=1)
        assert exc_info.match("Triplet length is 1, but value contains only 0 bytes")

    def test_from_bytes_missing_bytes_value(self: "TestTriplet") -> None:
        with pytest.raises(t.TripletMissingBytesError) as exc_info:
            t.Triplet(tag=DEFAULT_TAG, length=2, value=b"\x01")
        assert exc_info.match("Triplet length is 2, but value contains only 1 bytes")
