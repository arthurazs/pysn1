from pysn1.debugger import Identifier, IdentifierClass, PrimitiveType, ContextType, ApplicationType


# TODO @arthurazs: add from_bytes
class TestDebuggerFromInt:
    def test_from_int_universal(self: "TestDebuggerFromInt") -> None:
        identifier = Identifier.from_int(0b0000_0000)
        assert identifier.reference == IdentifierClass.UNIVERSAL
        assert identifier.primitive is True
        assert identifier.constructed is False
        assert identifier.datatype == PrimitiveType.END_OF_CONTENT
        assert int(identifier) == 0x00

    def test_from_int_application(self: "TestDebuggerFromInt") -> None:
        identifier = Identifier.from_int(0b0100_0000)
        assert identifier.reference == IdentifierClass.APPLICATION
        assert identifier.primitive is True
        assert identifier.constructed is False
        assert identifier.datatype == ApplicationType(value=0)
        assert int(identifier) == 0x40

    def test_from_int_context(self: "TestDebuggerFromInt") -> None:
        identifier = Identifier.from_int(0b1000_0000)
        assert identifier.reference == IdentifierClass.CONTEXT
        assert identifier.primitive is True
        assert identifier.constructed is False
        assert identifier.datatype == ContextType(value=0)
        assert int(identifier) == 0x80

    def test_from_int_private(self: "TestDebuggerFromInt") -> None:
        identifier = Identifier.from_int(0b1100_0000)
        assert identifier.reference == IdentifierClass.PRIVATE
        assert identifier.primitive is True
        assert identifier.constructed is False
        assert identifier.datatype == PrimitiveType.END_OF_CONTENT
        assert int(identifier) == 0xC0

    def test_from_int_constructed(self: "TestDebuggerFromInt") -> None:
        identifier = Identifier.from_int(0b0010_0000)
        assert identifier.reference == IdentifierClass.UNIVERSAL
        assert identifier.primitive is False
        assert identifier.constructed is True
        assert identifier.datatype == PrimitiveType.END_OF_CONTENT
        assert int(identifier) == 0x20

    def test_from_int_boolean(self: "TestDebuggerFromInt") -> None:
        identifier = Identifier.from_int(0b0000_0001)
        assert identifier.reference == IdentifierClass.UNIVERSAL
        assert identifier.primitive is True
        assert identifier.constructed is False
        assert identifier.datatype == PrimitiveType.BOOLEAN
        assert int(identifier) == 0x01

    def test_from_int_application_value(self: "TestDebuggerFromInt") -> None:
        identifier = Identifier.from_int(0b0100_0001)
        assert identifier.reference == IdentifierClass.APPLICATION
        assert identifier.primitive is True
        assert identifier.constructed is False
        assert identifier.datatype == ApplicationType(value=1)
        assert int(identifier) == 0x41

    def test_from_int_context_value(self: "TestDebuggerFromInt") -> None:
        identifier = Identifier.from_int(0b1000_0001)
        assert identifier.reference == IdentifierClass.CONTEXT
        assert identifier.primitive is True
        assert identifier.constructed is False
        assert identifier.datatype == ContextType(value=1)
        assert int(identifier) == 0x81