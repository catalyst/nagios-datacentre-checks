#!/usr/bin/env python
# coding: utf-8
#
# Copyright (c) 2015 Catalyst.net Ltd
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

"""
Extract information from an easYgen-1000 generator controller using Modbus over TCP.

Tobi Schulmann <tobias.schulmann@catalyst.net.nz> and Michael Fincham <michael.fincham@catalyst.net.nz>
"""

from pymodbus.client.sync import ModbusTcpClient
from contextlib import contextmanager

class EasygenInterface(object):

    registers = (
        (50001, "Protocol-ID"),
        (50002, "Generator: Voltage V L12 (0.1V)"),
        (50004, "Generator: Frequency (0.01 Hz)"),
        (50005, "Generator: Voltage V L1N (0.1V)"),
        (50007, "Mains: Frequency f 123 (0.01 Hz)"),
        (50008, "Generator: Voltage V L23 (0.1V)"),
        (50010, "Generator: Power factor cosφ L1 (0.001)"),
        (50011, "Generator: Voltage V L2N (0.1V)"),
        (50013, "Mains: Power factor cosφ L1 (0.001)"),
        (50014, "Generator: Voltage V L31 (0.1V)"),
        (50016, "Engine speed (RPM)"),
        (50017, "Generator: Voltage V L3N (0.1V)"),
        (50019, "Battery voltage (0.1V)"),
        (50020, "Mains: Voltage V L12 (0.1V)"),
        (50022, "Analog input [T1]"),
        (50023, "Mains: Voltage V L1N (0.1V)"),
        (50025, "Analog input [T2]"),
        (50026, "Mains: Voltage V L23 (0.1V)"),
        (50028, "Discrete inputs, status"),
        (50029, "Mains: Voltage V L23 (0.1V)"),
        (50031, "Relay outputs, status"),
        (50032, "Mains: Voltage V L31 (0.1V)"),
        (50034, "System status low"),
        (50035, "Mains: Voltage V L2N (0.1V)"),
        (50037, "Alarm classes"),
        (50038, "Generator: Current I L1 (mA)"),
        (50040, "Discrete inputs with alarm class"),
        (50041, "Generator: Current I L2 (mA)"),
        (50043, "Alarms 1"),
        (50044, "Generator: Current I L3 (mA)"),
        (50046, "Generator, watchdog 1"),
        (50047, "Mains: Current I L1 (mA)"),
        (50049, "Mains, watchdog 1"),
        (50050, "Generator: Reactive power Q (var)"),
        (50052, "Analog inputs, wire break"),
        (50053, "Generator: Real power P (W)"),
        (50055, "Analog inputs"),
        (50056, "Mains: Real power P L1 (W)"),
        (50058, "System status high"),
        (50059, "Mains: Reactive power Q (Q)"),
        (50061, "Generator: power factor cosφ (0.01)"),
        (50062, "Mains: power factor cosphi (0.01)"),
        (50063, "Mains: reactive power Q (0.1 kvar)"),
        (50064, "Generator: real power P (0.1 kW)"),
        (50065, "Generator: reactive power Q (0.1 kvar)"),
        (50066, "Mains: real power P (0.1 kW)"),
        (50067, "Generator, watchdog 2"),
        (50068, "Real energy (0.01 MWh)"),
        (50070, "Flag of the LogicsManager"),
        (50071, "Reactive energy (0.01 Mvarh)"),
        (50073, "Parameter 10202"),
        (50074, "Generator: Calculated ground current (mA)"),
        (50076, "External discrete inputs with alarm class"),
        (50077, "Parameter 10308"),
        (50079, "External relay outputs, status"),
        (50080, "External discrete inputs, status")
    )

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.cli = ModbusTcpClient(self.host, port=self.port)
        self.names, self.registers = self._get_mapping()

    def _get_mapping(self):
        names, registers = {}, {}
        i = 0
        last_reg = None
        for reg in EasygenInterface.registers:
            if last_reg:
                i += (reg[0] - last_reg)
            last_reg = reg[0]
            names[reg[1]] = i
            registers[reg[0]] = i

        return names, registers        

    def get_data_by_name(self, name):
        return self.data.registers[self.names[name]]

    def get_data_by_register(self, register):
        return self.data.registers[self.registers[register]]

    @contextmanager
    def connect(self):
        try:
            self.cli.connect()
            yield self.cli
        finally:
            self.cli.close()

    def fetch_registers(self, *args):
        """
        Retrieve and cache the latest data from the controller. Should be called before the get_data_by methods.
        """
        
        if args:
            start, number = args
        else:
            start = EasygenInterface.registers[0][0]
            number = EasygenInterface.registers[-1][0] + 1 - start

        with self.connect() as con:
            self.data = con.read_input_registers(start - 1, number, unit=0x01)
