#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Chemical substances and its properties."""

from tables import SaturatedWaterTable
from units import Celcius, Temperature, KJPerKg, UndefinedUnit


class UnknownState(Exception):
    pass


class SaturatedWater(object):
    """Abstraction of saturated water."""

    _table = SaturatedWaterTable

    def __init__(self, temperature=None, pressure=None, T=None, P=None):
        """The substance instance have temperature or pressure."""
        self.temperature = temperature or T
        self.pressure = pressure or P
        if not temperature and not pressure:
            raise UnknownState("Pressure or temperature is needed")
        elif temperature and pressure:
            raise UnknownState("Pressure and temperature are related properties")
        elif not isinstance(temperature, Temperature):
            raise UndefinedUnit("Temperature unit instance is needed")
        self._set_state()

    def _find_state(self):
        """Find thermodynamics state of the substance with given properties."""
        t = Celcius(self.temperature).value
        return self._table.find_state("temperature", t)

    def _set_state(self):
        """Set instance atributes for given state."""
        data = self._find_state()
        self.temperature = data[0]
        self.pressure = data[1]
        self.volume_liquid = data[2]
        self.volume_vapor = data[3]
        self.energy_liquid = KJPerKg(data[4])
        self.energy_vaporisation = KJPerKg(data[5])
        self.energy_vapor = KJPerKg(data[6])
        self.enthalpy_liquid = KJPerKg(data[7])
        self.enthalpy_vaporisation = KJPerKg(data[8])
        self.enthalpy_vapor = KJPerKg(data[9])
        self.entropy_liquid = data[10]
        self.entropy_vaporization = data[11]
        self.entropy_vapor = data[12]
