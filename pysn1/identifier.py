from dataclasses import dataclass
from enum import Enum
from typing import Protocol


class TypeProtocol(Protocol):
    name: str
    value: int


class IdentifierClass(Enum):
    UNIVERSAL = 0
    APPLICATION = 1
    CONTEXT = 2
    PRIVATE = 3


class IdentifierType(Enum):
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


@dataclass(frozen=True, kw_only=True, slots=True)
class Specific:
    value: int


class ContextSpecific(Specific):
    name: str = "Position"


class ApplicationSpecific(Specific):
    name: str = "Application"


# TODO @arthurazs: change into frozen dataclass, add Identifier.from_int()
class Identifier:

    __slots__ = ("_integer", "_reference", "_constructed", "_datatype")

    def __init__(self: "Identifier", integer: int) -> None:
        self._integer = integer
        self._reference = IdentifierClass(integer >> 6)  # 0b1100_0000

        # 0 for primitive, 1 for constructed
        self._constructed = bool(integer >> 5 & 0b1)  # 0b0010_0000

        # 0b0001_1111
        self._datatype: TypeProtocol  # TODO @arthurazs: fix protocol
        match self._reference.value:
            case IdentifierClass.APPLICATION.value:
                self._datatype = ApplicationSpecific(value=integer & 0x1F)
            case IdentifierClass.CONTEXT.value:
                self._datatype = ContextSpecific(value=integer & 0x1F)
            case _:
                self._datatype = IdentifierType(integer & 0x1F)

    def __int__(self: "Identifier") -> int:
        return self._integer

    @property
    def reference(self: "Identifier") -> IdentifierClass:
        return self._reference

    @property
    def primitive(self: "Identifier") -> bool:
        return not self._constructed

    @property
    def constructed(self: "Identifier") -> bool:
        return self._constructed

    @property
    def datatype(self: "Identifier") -> TypeProtocol:
        return self._datatype

    def debug(self: "Identifier") -> str:
        string = self._reference.name.capitalize()
        if self._constructed:
            string = f"{string} [Constructed]"
        string += ": "
        if isinstance(self._datatype, Specific):
            string += str(self._datatype.value)
        else:
            string += self._datatype.name.capitalize()
            if self._constructed:
                " " + str(self._datatype.value)
        string += f"\nint: {self._integer}"
        string += f"\nhex: {self._integer:#x}"
        string += f"\nbin: {self._integer:#_b}"
        return string
