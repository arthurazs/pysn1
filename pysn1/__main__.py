import logging

from pysn1.identifier import Identifier

logging.basicConfig(format="", level=logging.INFO)
logger = logging.getLogger(__package__)

identifier = Identifier(0b0010_0001)
logger.info(identifier.debug())
