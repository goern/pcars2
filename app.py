#!/usr/bin/env python3
# thoth-adviser
# Copyright(C) 2021 Christoph Görn 
#
# This program is free software: you can redistribute it and / or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
# type: ignore

"""."""

import logging
import os
import json
from runpy import run_module
from time import sleep

import click

from thoth.common import init_logging
from pcars2.packet import Packet

from pcars2.stream import PCarsStreamReceiver


__version__ = "0.1.0"

init_logging()

_LOGGER = logging.getLogger("sms_udp2mqtt")

class AMS2Listener(object):
    def handlePacket(self, data: Packet):
        _LOGGER.debug(json.dumps(data.__dict__))

        if data.packetType == 0:
            _LOGGER.info(f"{data['sequenceNumber']}: speed={data['speed']}")

def _print_version(ctx: click.Context, _, value: str):
    """Print version and exit."""
    if not value or ctx.resilient_parsing:
        return

    click.echo(__version__)
    ctx.exit()



@click.command()
@click.pass_context
@click.option(
    "-v",
    "--verbose",
    is_flag=True,
    envvar="DEBUG",
    help="Be verbose about what's going on.",
)
@click.option(
    "--version",
    is_flag=True,
    is_eager=True,
    callback=_print_version,
    expose_value=False,
    help="Print version and exit.",
)
def cli(ctx=None, verbose=False):
    if ctx:
        ctx.auto_envvar_prefix = "THOTH_ADVISER"

    if verbose:
        _LOGGER.setLevel(logging.DEBUG)

    _LOGGER.debug("Debug mode is on")
    _LOGGER.info("#B4mad SimRace Telemetry sms_udp2mqtt v%s", __version__)

    listener = AMS2Listener()
    stream = PCarsStreamReceiver()
    stream.addListener(listener)
    stream.run()

__name__ == "__main__" and cli()
