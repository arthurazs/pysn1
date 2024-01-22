import pytest
from pysn1.debugger import Identifier, IdentifierClass, PrimitiveType, ContextType, ApplicationType


class TestIdentifier:
    def test_from_int_universal(self: "TestIdentifier") -> None:
        identifier = Identifier.from_int(0b0000_0000)
        assert identifier.reference == IdentifierClass.UNIVERSAL
        assert identifier.primitive is True
        assert identifier.constructed is False
        assert identifier.datatype == PrimitiveType.END_OF_CONTENT
        assert int(identifier) == 0x00

    def test_from_int_application(self: "TestIdentifier") -> None:
        identifier = Identifier.from_int(0b0100_0000)
        assert identifier.reference == IdentifierClass.APPLICATION
        assert identifier.primitive is True
        assert identifier.constructed is False
        assert identifier.datatype == ApplicationType(value=0)
        assert int(identifier) == 0x40

    def test_from_int_context(self: "TestIdentifier") -> None:
        identifier = Identifier.from_int(0b1000_0000)
        assert identifier.reference == IdentifierClass.CONTEXT
        assert identifier.primitive is True
        assert identifier.constructed is False
        assert identifier.datatype == ContextType(value=0)
        assert int(identifier) == 0x80

    def test_from_int_private(self: "TestIdentifier") -> None:
        identifier = Identifier.from_int(0b1100_0000)
        assert identifier.reference == IdentifierClass.PRIVATE
        assert identifier.primitive is True
        assert identifier.constructed is False
        assert identifier.datatype == PrimitiveType.END_OF_CONTENT
        assert int(identifier) == 0xC0

    def test_from_int_constructed(self: "TestIdentifier") -> None:
        identifier = Identifier.from_int(0b0010_0000)
        assert identifier.reference == IdentifierClass.UNIVERSAL
        assert identifier.primitive is False
        assert identifier.constructed is True
        assert identifier.datatype == PrimitiveType.END_OF_CONTENT
        assert int(identifier) == 0x20

    def test_from_int_boolean(self: "TestIdentifier") -> None:
        identifier = Identifier.from_int(0b0000_0001)
        assert identifier.reference == IdentifierClass.UNIVERSAL
        assert identifier.primitive is True
        assert identifier.constructed is False
        assert identifier.datatype == PrimitiveType.BOOLEAN
        assert int(identifier) == 0x01
