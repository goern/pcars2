import logging
import os
import json
from runpy import run_module
from time import sleep

from thoth.common import init_logging
from pcars2.packet import Packet

from pcars2.stream import PCarsStreamReceiver


__version__ = "0.1.0"

init_logging()

# set up logging
DEBUG_LEVEL = bool(int(os.getenv("DEBUG_LEVEL", 1)))

if DEBUG_LEVEL:
    logging.basicConfig(level=logging.DEBUG)
else:
    logging.basicConfig(level=logging.INFO)

_LOGGER = logging.getLogger(__name__)
_LOGGER.info("#B4mad SimRace Telemetry v%s", __version__)


class AMS2Listener(object):
    def handlePacket(self, data: Packet):
        _LOGGER.debug(json.dumps(data.__dict__))

        if data.packetType == 0:
            _LOGGER.info(json.dumps(data["speed"]))

if __name__ == "__main__":
    listener = AMS2Listener()
    stream = PCarsStreamReceiver()
    stream.addListener(listener)
    stream.run()
