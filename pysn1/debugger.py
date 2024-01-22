from dataclasses import dataclass
from enum import Enum
from struct import pack, unpack
from typing import Protocol


class TypeProtocol(Protocol):

    @property
    def name(self: "TypeProtocol") -> str:
        ...

    @property
    def value(self: "TypeProtocol") -> int:
        ...

    def __int__(self: "TypeProtocol") -> int:
        ...


class IdentifierClass(Enum):
    UNIVERSAL = 0
    APPLICATION = 1
    CONTEXT = 2
    PRIVATE = 3

    def __int__(self: "IdentifierClass") -> int:
        return self.value


class PrimitiveType(Enum):
    END_OF_CONTENT = 0
    BOOLEAN = 1
    INTEGER = 2
    BIT_STRING = 3
    OCTET_STRING = 4
    NULL = 5
    OBJECT_IDENTIFIER = 6
    OBJECT_DESCRIPTOR = 7
    EXTERNAL = 8
    REAL = 9
    ENUMERATED = 10
    EMBEDDED_PDV = 11
    UTF8_STRING = 12
    RELATIVE_OID = 13
    TIME = 14
    RESERVED = 15
    SEQUENCE_OF = 16
    SET_OF = 17
    NUMERIC_STRING = 18
    PRINTABLE_STRING = 19
    T61STRING = 20
    VIDEOTEX_STRING = 21
    IA5STRING = 22
    UTC_TIME = 23
    GENERALIZED_TIME = 24
    GRAPHIC_STRING = 25
    VISIBLE_STRING = 26
    GENERAL_STRING = 27
    UNIVERSAL_STRING = 28
    CHARACTER_STRING = 29
    BMP_STRING = 30
    DATE = STRING = 31
    TIME_OF_DAY = 32
    DATE_TIME = 33
    DURATION = 34
    OID_IRI = 35
    RELATIVE_OID_IRI = 36

    def __int__(self: "PrimitiveType") -> int:
        return self.value


@dataclass(frozen=True, kw_only=True, slots=True)
class SpecificType:  # TODO theres probably a better way to do this
    value: int

    def __repr__(self: "SpecificType") -> str:
        class_name = self.__class__.__name__
        object_name = self.name  # type: ignore[attr-defined]
        object_value = self.value
        return f"<{class_name}.{object_name}: {object_value}>"

    def __int__(self: "SpecificType") -> int:
        return self.value


class ContextType(SpecificType):
    name: str = "POSITION"


class ApplicationType(SpecificType):
    name: str = "APPLICATION"


@dataclass(frozen=True, kw_only=True, slots=True)
class Identifier:

    reference: IdentifierClass = IdentifierClass.UNIVERSAL
    constructed: bool = False
    datatype: TypeProtocol = PrimitiveType.BOOLEAN

    @classmethod
    def from_int(cls: type["Identifier"], integer: int) -> "Identifier":
        ref = IdentifierClass(integer >> 6)  # 0b1100_0000

        # 0 for primitive, 1 for constructed
        constructed = bool(integer >> 5 & 0b1)  # 0b0010_0000

        # 0b0001_1111
        datatype: TypeProtocol  # TODO fix protocol
        match ref.value:
            case IdentifierClass.APPLICATION.value:
                datatype = ApplicationType(value=integer & 0x1F)
            case IdentifierClass.CONTEXT.value:
                datatype = ContextType(value=integer & 0x1F)
            case _:
                datatype = PrimitiveType(integer & 0x1F)
        return cls(reference=ref, constructed=constructed, datatype=datatype)

    @classmethod
    def from_bytes(cls: type["Identifier"], bytestring: bytes) -> "Identifier":
        return cls.from_int(unpack("!B", bytestring)[0])

    def __int__(self: "Identifier") -> int:
        ref = int(self.reference)
        pc = int(self.constructed)
        dt = int(self.datatype)
        return (ref << 6) + (pc << 5) + dt

    @property
    def integer(self: "Identifier") -> int:
        return int(self)

    @property
    def primitive(self: "Identifier") -> bool:
        return not self.constructed

    def __bytes__(self: "Identifier") -> bytes:
        return pack("!B", int(self))

    def __str__(self: "Identifier") -> str:
        string = repr(self) + "\n"
        string += self.reference.name.capitalize()
        if self.constructed:
            string = f"{string} [Constructed]"
        string += ": "
        if isinstance(self.datatype, SpecificType):
            string += str(self.datatype.value)
        else:
            string += self.datatype.name.capitalize()
            if self.constructed:
                " " + str(self.datatype.value)
        string += f"\nint: {int(self)}"
        string += f"\nhex: {int(self):#x}"
        string += f"\nbin: {int(self):#011_b}"

        string += f"\nbyt: {bytes(self)!s:>7} [ASCII]"
        in_bytes = hex(int(self)).replace("0x", "")
        if len(in_bytes) == 1:
            in_bytes = "0" + in_bytes
        string += f"\nbyt: b'\\x{in_bytes}' [No-ASCII]"
        return string
