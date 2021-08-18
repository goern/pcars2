#!/usr/bin/env python3
#
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
import json

import paho.mqtt.client as mqtt

import time


def on_message(client, userdata, message):
    print("received message: ", str(message.payload.decode("utf-8")))


mqttBroker = "mqtt.eclipseprojects.io"

client = mqtt.Client("b4mad.sms_udp_dump")
client.connect(mqttBroker)

client.loop_start()

client.subscribe("b4mad.sms_udp.ams2")
client.on_message = on_message

time.sleep(30)
client.loop_stop()
