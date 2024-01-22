from dataclasses import dataclass
from struct import unpack

EXTENDED_LENGTH = 0x80
MAX_EXTENDED_LENGTH = 0x84
EXTENDED_LENGTH_1 = 0xFF
EXTENDED_LENGTH_2 = 0xFFFF
EXTENDED_LENGTH_3 = 0xFFFFFF
EXTENDED_LENGTH_4 = 0xFFFFFFFF


class TripletLengthTooBigError(ValueError):

    def __init__(
            self: "TripletLengthTooBigError",
            msg: str = "Triplet with extended length > 4 not implemented",
    ) -> None:
        super().__init__(msg)


class TripletMissingBytesError(ValueError): ...


class TripletTooManyBytesError(ValueError): ...


class TripletBadLengthError(ValueError): ...


@dataclass(frozen=True, kw_only=True, slots=True)
class Triplet:
    tag: int
    length: int
    value: bytes

    def __len__(self: "Triplet") -> int:
        # tag field + len field + value field len
        length = 1 + 1 + len(self.value)
        if self.length < EXTENDED_LENGTH:
            return length
        if self.length <= EXTENDED_LENGTH_1:
            return length + 1
        if self.length <= EXTENDED_LENGTH_2:
            return length + 2
        if self.length <= EXTENDED_LENGTH_3:
            return length + 3
        if self.length <= EXTENDED_LENGTH_4:
            return length + 4
        raise TripletLengthTooBigError

    def __bytes__(self: "Triplet") -> bytes:
        # TODO @arthurazs: triplet to bytes
        return b""

    @staticmethod
    def _find_length(length: int, extended_length_string: bytes) -> tuple[int, int]:
        extended_length = 0
        if length > EXTENDED_LENGTH and not extended_length_string:
            msg = "Triplet extended length is missing bytes"
            raise TripletMissingBytesError(msg)

        match length:
            case 0x81:
                length = unpack("!B", extended_length_string[0:1])[0]
                extended_length = 1
            case 0x82:
                length = unpack("!H", extended_length_string[0:2])[0]
                extended_length = 2
            case 0x83:
                length = unpack("!I", b"\x00" + extended_length_string[0:3])[0]
                extended_length = 3
            case 0x84:
                length = unpack("!I", extended_length_string[0:4])[0]
                extended_length = 4
            case _ if length > MAX_EXTENDED_LENGTH:
                raise TripletLengthTooBigError

        if length < EXTENDED_LENGTH and extended_length > 0:
            msg = "Triplet contains extended length, but extended length is less than 128 (0x80)"
            raise TripletBadLengthError(msg)
        return length, extended_length

    @classmethod
    def from_bytes(cls: type["Triplet"], bytestring: bytes) -> "Triplet":
        tag = unpack("!B", bytestring[0:1])[0]

        # length in pos 1, extended_length possibly in pos 2+
        length, extended_length = cls._find_length(unpack("!B", bytestring[1:2])[0], bytestring[2:6])

        # value comes after tag (pos 0) and length (pos 1) and extended_length (possibly pos 2+)
        value = bytestring[2 + extended_length:]

        if length > len(value):
            msg = f"Triplet length is {length}, but value contains only {len(value)} bytes"
            raise TripletMissingBytesError(msg)
        if length < len(value):
            msg = f"Triplet length is {length}, but value contains {len(value)} bytes"
            raise TripletTooManyBytesError(msg)

        return Triplet(tag=tag, length=length, value=value)
