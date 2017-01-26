#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Chemical substances and its properties."""

from tables import SaturatedWaterTable
from units import UndefinedUnit, GenericUnit, UnitMismatch
from units.temperature import Celcius
from units.pressure import KiloPascal
from units.energy import KJPerKg

__dir__ = ['SaturationLineWater', 'SaturatedWater', 'SaturatedSteam']
__all__ = __dir__


class UnknownState(Exception):
    pass


class SaturationLineWater(object):
    """Abstraction of saturated water."""

    name = "Water on saturation line"
    _table = SaturatedWaterTable

    def __init__(self, property_state):
        """The substance instance need one known property value."""
        if not isinstance(property_state, GenericUnit):
            raise UndefinedUnit("Unit instance is needed")
        self._set_state(property_state)

    def _find_state(self, property_state):
        """Find thermodynamics state of the substance with given properties."""
        required_units = {"temperature": Celcius,
                          "pressure": KiloPascal}
        unit_class = required_units[property_state.property_name]
        if not property_state.issameproperty(unit_class):
            raise UnitMismatch("%s %s" % (property_state.__class__, unit_class))
        value = unit_class(property_state).value
        return self._table.find_state(property_state.property_name, value)

    def _set_state(self, property_state):
        """Set instance atributes for given state."""
        data = self._find_state(property_state)
        self.temperature = Celcius(data[0])
        self.pressure = KiloPascal(data[1])
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

    def __unicode__(self):
        """Unicode representation."""
        return u"%s at %s" % (self.name, self.temperature)

    def __str__(self):
        """String representation."""
        return self.__unicode__().encode("utf-8")

    def __repr__(self):
        """Short representation."""
        return self.__str__()


class SaturatedWater(SaturationLineWater):
    """Liquid water on saturated state."""

    name = "Saturated water"

    def _set_state(self, property_state):
        """Set instance atributes for given state."""
        data = self._find_state(property_state)
        self.temperature = Celcius(data[0])
        self.pressure = KiloPascal(data[1])
        self.volume = data[2]
        self.energy = KJPerKg(data[4])
        self.enthalpy = KJPerKg(data[7])
        self.entropy = data[10]


class SaturatedSteam(SaturationLineWater):
    """Liquid water on saturated state."""

    name = "Saturated steam"

    def _set_state(self, property_state):
        """Set instance atributes for given state."""
        data = self._find_state(property_state)
        self.temperature = Celcius(data[0])
        self.pressure = KiloPascal(data[1])
        self.volume = data[3]
        self.energy = KJPerKg(data[6])
        self.enthalpy = KJPerKg(data[9])
        self.entropy = data[12]
