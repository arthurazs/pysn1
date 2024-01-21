import pytest
from pysn1.identifier import Identifier, IdentifierClass, IdentifierType, ContextSpecific, ApplicationSpecific


class TestIdentifier:
    def test_creation(self: "TestIdentifier") -> None:
        identifier = Identifier(0)
        assert identifier.reference == IdentifierClass.UNIVERSAL
        assert identifier.primitive is True
        assert identifier.constructed is False
        assert identifier.datatype == IdentifierType.END_OF_CONTENT
        assert int(identifier) == 0
        # TODO @arthurazs: necessary?
        with pytest.raises(AttributeError):
            identifier.reference = 1
        with pytest.raises(AttributeError):
            identifier.primitive = 1
        with pytest.raises(AttributeError):
            identifier.constructed = 1
        with pytest.raises(AttributeError):
            identifier.datatype = 1
