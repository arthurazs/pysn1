from dataclasses import dataclass
from struct import pack, unpack

EXTENDED_LENGTH = 0x80
MAX_EXTENDED_LENGTH = 0x84
EXTENDED_LENGTH_1 = 0xFF
EXTENDED_LENGTH_2 = 0xFFFF
EXTENDED_LENGTH_3 = 0xFFFFFF
EXTENDED_LENGTH_4 = 0xFFFFFFFF
NO_EXTRA_BYTES = 0
ONE_EXTRA_BYTE = 1
TWO_EXTRA_BYTES = 2
THREE_EXTRA_BYTES = 3
FOUR_EXTRA_BYTES = 4

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
    value: bytes = b""

    def __post_init__(self: "Triplet") -> None:
        if self.length > EXTENDED_LENGTH_4:
            raise TripletLengthTooBigError
        if self.length > len(self.value):
            msg = f"Triplet length is {self.length}, but value contains only {len(self.value)} bytes"
            raise TripletMissingBytesError(msg)
        if self.length < len(self.value):
            msg = f"Triplet length is {self.length}, but value contains {len(self.value)} bytes"
            raise TripletTooManyBytesError(msg)

    def _extended_length(self: "Triplet") -> int:
        if self.length < EXTENDED_LENGTH:
            return NO_EXTRA_BYTES
        if self.length <= EXTENDED_LENGTH_1:
            return ONE_EXTRA_BYTE
        if self.length <= EXTENDED_LENGTH_2:
            return TWO_EXTRA_BYTES
        if self.length <= EXTENDED_LENGTH_3:
            return THREE_EXTRA_BYTES
        if self.length <= EXTENDED_LENGTH_4:
            return FOUR_EXTRA_BYTES
        raise TripletLengthTooBigError

    def __len__(self: "Triplet") -> int:
        # tag field + len field + value field len + extended length
        return 1 + 1 + len(self.value) + self._extended_length()

    @classmethod
    def build(cls: type["Triplet"], tag: int, value: bytes) -> "Triplet":
        return cls(tag=tag, length=len(value), value=value)

    def __bytes__(self: "Triplet") -> bytes:
        tag = pack("!B", self.tag)
        extended_length = self._extended_length()
        if extended_length == NO_EXTRA_BYTES:
            length = pack("!B", self.length)
        elif extended_length == ONE_EXTRA_BYTE:
            length = b"\x81" + pack("!B", self.length)
        elif extended_length == TWO_EXTRA_BYTES:
            length = b"\x82" + pack("!H", self.length)
        elif extended_length == THREE_EXTRA_BYTES:
            length = b"\x83" + pack("!I", self.length)[1:4]
        elif extended_length == FOUR_EXTRA_BYTES:
            length = b"\x84" + pack("!I", self.length)
        else:
            raise TripletLengthTooBigError
        return tag + length + self.value

    @staticmethod
    def _find_length(length: int, extended_length_string: bytes) -> tuple[int, int]:
        extended_length = 0
        if length > EXTENDED_LENGTH and not extended_length_string:
            msg = "Triplet extended length is missing bytes"
            raise TripletMissingBytesError(msg)

        match length:
            case 0x81:
                length = unpack("!B", extended_length_string[0:1])[0]
                extended_length = ONE_EXTRA_BYTE
            case 0x82:
                length = unpack("!H", extended_length_string[0:2])[0]
                extended_length = TWO_EXTRA_BYTES
            case 0x83:
                length = unpack("!I", b"\x00" + extended_length_string[0:3])[0]
                extended_length = THREE_EXTRA_BYTES
            case 0x84:
                length = unpack("!I", extended_length_string[0:4])[0]
                extended_length = FOUR_EXTRA_BYTES
            case _ if length > MAX_EXTENDED_LENGTH:
                raise TripletLengthTooBigError

        if length < EXTENDED_LENGTH and extended_length > NO_EXTRA_BYTES:
            msg = "Triplet contains extended length, but extended length is less than 128 (0x80)"
            raise TripletBadLengthError(msg)
        return length, extended_length

    @classmethod
    def from_bytes(cls: type["Triplet"], bytestring: bytes) -> "Triplet":
        tag = unpack("!B", bytestring[0:1])[0]

        # length in pos 1, extended_length possibly in pos 2+
        length, extended_length = cls._find_length(unpack("!B", bytestring[1:2])[0], bytestring[2:6])

        # value comes after tag (pos 0) and length (pos 1) and extended_length (possibly pos 2+)
        start = 2 + extended_length
        end = start + length
        value = bytestring[start:end]

        if length > len(value):
            msg = f"Triplet length is {length}, but value contains only {len(value)} bytes"
            raise TripletMissingBytesError(msg)

        return Triplet(tag=tag, length=length, value=value)

    def debug(self: "Triplet") -> str:
        string = repr(self) + "\n"
        string += f"{self.tag=:#04x}, {self.length=:#04x}\n"
        string += f"{self.tag=}, {self.length=}: {self.value!r}\n"
        string += f"{len(self)=}\n"
        string += f"{bytes(self)=}"
        return string
