import logging

from pysn1.debugger import Identifier
from pysn1.triplet import Triplet

logging.basicConfig(format="", level=logging.INFO)
logger = logging.getLogger(__package__)

identifier = Identifier.from_bytes(b"\x01")
logger.info(str(identifier))

t1 = Triplet(tag=1, length=1, value=b"\x01")
t2 = Triplet.from_bytes(b"\x01\x01\x01")

logger.info(t1)
logger.info(t2)
logger.info(t1.debug())
