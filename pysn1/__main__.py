import logging

from pysn1.debugger import Identifier

logging.basicConfig(format="", level=logging.INFO)
logger = logging.getLogger(__package__)

identifier = Identifier.from_bytes(b"\x01")
logger.info(str(identifier))
