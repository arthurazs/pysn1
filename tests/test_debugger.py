from pysn1.debugger import ApplicationType, ContextType, Identifier, IdentifierClass, PrimitiveType


class TestDebugger:
    def test_identifier_bugs(self: "TestDebugger") -> None:
        # TODO @arthurazs: implement exceptions for bad identifiers
        # which class should allow constructed?
        # which primitive types should allow constructed?
        pass

    def test_identifier_universal(self: "TestDebugger") -> None:
        identifier = Identifier(
            reference=IdentifierClass.UNIVERSAL,
            constructed=False,
            datatype=PrimitiveType.END_OF_CONTENT,
        )
        assert identifier.reference == IdentifierClass.UNIVERSAL
        assert identifier.primitive is True
        assert identifier.constructed is False
        assert identifier.datatype == PrimitiveType.END_OF_CONTENT
        assert int(identifier) == 0x00
        assert bytes(identifier) == b"\x00"

    def test_identifier_application(self: "TestDebugger") -> None:
        identifier = Identifier(
            reference=IdentifierClass.APPLICATION,
            constructed=False,
            datatype=ApplicationType(value=0),
        )
        assert identifier.reference == IdentifierClass.APPLICATION
        assert identifier.primitive is True
        assert identifier.constructed is False
        assert identifier.datatype == ApplicationType(value=0)
        assert int(identifier) == 0x40  # noqa: PLR2004
        assert bytes(identifier) == b"\x40"

    def test_identifier_context(self: "TestDebugger") -> None:
        identifier = Identifier(reference=IdentifierClass.CONTEXT, constructed=False, datatype=ContextType(value=0))
        assert identifier.reference == IdentifierClass.CONTEXT
        assert identifier.primitive is True
        assert identifier.constructed is False
        assert identifier.datatype == ContextType(value=0)
        assert int(identifier) == 0x80  # noqa: PLR2004
        assert bytes(identifier) == b"\x80"

    def test_identifier_private(self: "TestDebugger") -> None:
        identifier = Identifier(
            reference=IdentifierClass.PRIVATE,
            constructed=False,
            datatype=PrimitiveType.END_OF_CONTENT,
        )
        assert identifier.reference == IdentifierClass.PRIVATE
        assert identifier.primitive is True
        assert identifier.constructed is False
        assert identifier.datatype == PrimitiveType.END_OF_CONTENT
        assert int(identifier) == 0xC0  # noqa: PLR2004
        assert bytes(identifier) == b"\xC0"

    def test_identifier_constructed(self: "TestDebugger") -> None:
        identifier = Identifier(
            reference=IdentifierClass.UNIVERSAL,
            constructed=True,
            datatype=PrimitiveType.END_OF_CONTENT,
        )
        assert identifier.reference == IdentifierClass.UNIVERSAL
        assert identifier.primitive is False
        assert identifier.constructed is True
        assert identifier.datatype == PrimitiveType.END_OF_CONTENT
        assert int(identifier) == 0x20  # noqa: PLR2004
        assert bytes(identifier) == b"\x20"

    def test_identifier_boolean(self: "TestDebugger") -> None:
        identifier = Identifier(reference=IdentifierClass.UNIVERSAL, constructed=False, datatype=PrimitiveType.BOOLEAN)
        assert identifier.reference == IdentifierClass.UNIVERSAL
        assert identifier.primitive is True
        assert identifier.constructed is False
        assert identifier.datatype == PrimitiveType.BOOLEAN
        assert int(identifier) == 0x01
        assert bytes(identifier) == b"\x01"

    def test_identifier_application_value(self: "TestDebugger") -> None:
        identifier = Identifier(
            reference=IdentifierClass.APPLICATION,
            constructed=False,
            datatype=ApplicationType(value=1),
        )
        assert identifier.reference == IdentifierClass.APPLICATION
        assert identifier.primitive is True
        assert identifier.constructed is False
        assert identifier.datatype == ApplicationType(value=1)
        assert int(identifier) == 0x41  # noqa: PLR2004
        assert bytes(identifier) == b"\x41"

    def test_identifier_context_value(self: "TestDebugger") -> None:
        identifier = Identifier(reference=IdentifierClass.CONTEXT, constructed=False, datatype=ContextType(value=1))
        assert identifier.reference == IdentifierClass.CONTEXT
        assert identifier.primitive is True
        assert identifier.constructed is False
        assert identifier.datatype == ContextType(value=1)
        assert int(identifier) == 0x81  # noqa: PLR2004
        assert bytes(identifier) == b"\x81"


class TestDebuggerFromInt:
    def test_from_int_universal(self: "TestDebuggerFromInt") -> None:
        identifier = Identifier.from_int(0b0000_0000)
        assert identifier.reference == IdentifierClass.UNIVERSAL
        assert identifier.primitive is True
        assert identifier.constructed is False
        assert identifier.datatype == PrimitiveType.END_OF_CONTENT
        assert int(identifier) == 0x00
        assert bytes(identifier) == b"\x00"

    def test_from_int_application(self: "TestDebuggerFromInt") -> None:
        identifier = Identifier.from_int(0b0100_0000)
        assert identifier.reference == IdentifierClass.APPLICATION
        assert identifier.primitive is True
        assert identifier.constructed is False
        assert identifier.datatype == ApplicationType(value=0)
        assert int(identifier) == 0x40  # noqa: PLR2004
        assert bytes(identifier) == b"\x40"

    def test_from_int_context(self: "TestDebuggerFromInt") -> None:
        identifier = Identifier.from_int(0b1000_0000)
        assert identifier.reference == IdentifierClass.CONTEXT
        assert identifier.primitive is True
        assert identifier.constructed is False
        assert identifier.datatype == ContextType(value=0)
        assert int(identifier) == 0x80  # noqa: PLR2004
        assert bytes(identifier) == b"\x80"

    def test_from_int_private(self: "TestDebuggerFromInt") -> None:
        identifier = Identifier.from_int(0b1100_0000)
        assert identifier.reference == IdentifierClass.PRIVATE
        assert identifier.primitive is True
        assert identifier.constructed is False
        assert identifier.datatype == PrimitiveType.END_OF_CONTENT
        assert int(identifier) == 0xC0  # noqa: PLR2004
        assert bytes(identifier) == b"\xC0"

    def test_from_int_constructed(self: "TestDebuggerFromInt") -> None:
        identifier = Identifier.from_int(0b0010_0000)
        assert identifier.reference == IdentifierClass.UNIVERSAL
        assert identifier.primitive is False
        assert identifier.constructed is True
        assert identifier.datatype == PrimitiveType.END_OF_CONTENT
        assert int(identifier) == 0x20  # noqa: PLR2004
        assert bytes(identifier) == b"\x20"

    def test_from_int_boolean(self: "TestDebuggerFromInt") -> None:
        identifier = Identifier.from_int(0b0000_0001)
        assert identifier.reference == IdentifierClass.UNIVERSAL
        assert identifier.primitive is True
        assert identifier.constructed is False
        assert identifier.datatype == PrimitiveType.BOOLEAN
        assert int(identifier) == 0x01
        assert bytes(identifier) == b"\x01"

    def test_from_int_application_value(self: "TestDebuggerFromInt") -> None:
        identifier = Identifier.from_int(0b0100_0001)
        assert identifier.reference == IdentifierClass.APPLICATION
        assert identifier.primitive is True
        assert identifier.constructed is False
        assert identifier.datatype == ApplicationType(value=1)
        assert int(identifier) == 0x41  # noqa: PLR2004
        assert bytes(identifier) == b"\x41"

    def test_from_int_context_value(self: "TestDebuggerFromInt") -> None:
        identifier = Identifier.from_int(0b1000_0001)
        assert identifier.reference == IdentifierClass.CONTEXT
        assert identifier.primitive is True
        assert identifier.constructed is False
        assert identifier.datatype == ContextType(value=1)
        assert int(identifier) == 0x81  # noqa: PLR2004
        assert bytes(identifier) == b"\x81"


class TestDebuggerFromBytes:
    def test_from_int_universal(self: "TestDebuggerFromBytes") -> None:
        identifier = Identifier.from_bytes(b"\x00")
        assert identifier.reference == IdentifierClass.UNIVERSAL
        assert identifier.primitive is True
        assert identifier.constructed is False
        assert identifier.datatype == PrimitiveType.END_OF_CONTENT
        assert int(identifier) == 0x00
        assert bytes(identifier) == b"\x00"

    def test_from_int_application(self: "TestDebuggerFromBytes") -> None:
        identifier = Identifier.from_bytes(b"\x40")
        assert identifier.reference == IdentifierClass.APPLICATION
        assert identifier.primitive is True
        assert identifier.constructed is False
        assert identifier.datatype == ApplicationType(value=0)
        assert int(identifier) == 0x40  # noqa: PLR2004
        assert bytes(identifier) == b"\x40"

    def test_from_int_context(self: "TestDebuggerFromBytes") -> None:
        identifier = Identifier.from_bytes(b"\x80")
        assert identifier.reference == IdentifierClass.CONTEXT
        assert identifier.primitive is True
        assert identifier.constructed is False
        assert identifier.datatype == ContextType(value=0)
        assert int(identifier) == 0x80  # noqa: PLR2004
        assert bytes(identifier) == b"\x80"

    def test_from_int_private(self: "TestDebuggerFromBytes") -> None:
        identifier = Identifier.from_bytes(b"\xC0")
        assert identifier.reference == IdentifierClass.PRIVATE
        assert identifier.primitive is True
        assert identifier.constructed is False
        assert identifier.datatype == PrimitiveType.END_OF_CONTENT
        assert int(identifier) == 0xC0  # noqa: PLR2004
        assert bytes(identifier) == b"\xC0"

    def test_from_int_constructed(self: "TestDebuggerFromBytes") -> None:
        identifier = Identifier.from_bytes(b"\x20")
        assert identifier.reference == IdentifierClass.UNIVERSAL
        assert identifier.primitive is False
        assert identifier.constructed is True
        assert identifier.datatype == PrimitiveType.END_OF_CONTENT
        assert int(identifier) == 0x20  # noqa: PLR2004
        assert bytes(identifier) == b"\x20"

    def test_from_int_boolean(self: "TestDebuggerFromBytes") -> None:
        identifier = Identifier.from_bytes(b"\x01")
        assert identifier.reference == IdentifierClass.UNIVERSAL
        assert identifier.primitive is True
        assert identifier.constructed is False
        assert identifier.datatype == PrimitiveType.BOOLEAN
        assert int(identifier) == 0x01
        assert bytes(identifier) == b"\x01"

    def test_from_int_application_value(self: "TestDebuggerFromBytes") -> None:
        identifier = Identifier.from_bytes(b"\x41")
        assert identifier.reference == IdentifierClass.APPLICATION
        assert identifier.primitive is True
        assert identifier.constructed is False
        assert identifier.datatype == ApplicationType(value=1)
        assert int(identifier) == 0x41  # noqa: PLR2004
        assert bytes(identifier) == b"\x41"

    def test_from_int_context_value(self: "TestDebuggerFromBytes") -> None:
        identifier = Identifier.from_bytes(b"\x81")
        assert identifier.reference == IdentifierClass.CONTEXT
        assert identifier.primitive is True
        assert identifier.constructed is False
        assert identifier.datatype == ContextType(value=1)
        assert int(identifier) == 0x81  # noqa: PLR2004
        assert bytes(identifier) == b"\x81"
