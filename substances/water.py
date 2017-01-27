#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Chemical substances and its properties."""

from substances.tables import SaturatedWaterTable
from units import UndefinedUnit, GenericUnit, UnitMismatch, UnitNotSupported
from units.temperature import Celcius
from units.pressure import KiloPascal
from units.energy import KJPerKg
from units.amount import CubicMeterPerKiloGram, Mass, Volume
from containers import Flask
from properties import GenericProperty, SpecificEnthalpy, Enthalpy

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
        if not any([isinstance(property_state, GenericUnit),
                    isinstance(property_state, GenericProperty)]):
            raise UndefinedUnit("Unit instance is needed")
        self._set_state(property_state)

    def _find_state(self, property_state):
        """Find thermodynamics state of the substance with given properties."""
        property_name = property_state.property_name
        if property_name == "temperature":
            value = Celcius(property_state).value
        elif property_name == "pressure":
            value = KiloPascal(property_state).value
        elif property_name == "enthalpy":
            raise UnknownState("Water saturation line have ambiguous enthalpy")
        else:
            raise UnitNotSupported("%s is not supported" % property_name)
        return self._table.find_state(property_name, value)

    def _set_state(self, property_state):
        """Set instance atributes for given state."""
        data = self._find_state(property_state)
        self.temperature = Celcius(data[0])
        self.pressure = KiloPascal(data[1])
        self.volume_liquid = CubicMeterPerKiloGram(data[2])
        self.volume_vapor = CubicMeterPerKiloGram(data[3])
        self.energy_liquid = KJPerKg(data[4])
        self.energy_vaporisation = KJPerKg(data[5])
        self.energy_vapor = KJPerKg(data[6])
        self.enthalpy_liquid = SpecificEnthalpy(KJPerKg(data[7]))
        self.enthalpy_vaporisation = SpecificEnthalpy(KJPerKg(data[8]))
        self.enthalpy_vapor = SpecificEnthalpy(KJPerKg(data[9]))
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

    def __mul__(self, multiplier):
        """Allow to multiply substance to amount and result a container."""
        if isinstance(multiplier, Mass) or isinstance(multiplier, Volume):
            return Flask(self, multiplier)
        else:
            return super(self.__class__, self).__mul__(multiplier)


class SaturatedWater(SaturationLineWater):
    """Liquid water on saturated state."""

    name = "Saturated water"

    def _find_state(self, property_state):
        """Find thermodynamics state of the substance with given properties."""
        if property_state.property_name == "specific enthalpy":
            property_name = "enthalpy_liquid"
            value = property_state.specific_energy.kJperkg.value
            return self._table.find_state(property_name, value)
        return super(SaturatedWater, self)._find_state(property_state)

    def _set_state(self, property_state):
        """Set instance atributes for given state."""
        data = self._find_state(property_state)
        self.temperature = Celcius(data[0])
        self.pressure = KiloPascal(data[1])
        self.volume = CubicMeterPerKiloGram(data[2])
        self.energy = KJPerKg(data[4])
        self.enthalpy = SpecificEnthalpy(KJPerKg(data[7]))
        self.enthalpy_vaporisation = SpecificEnthalpy(KJPerKg(data[8]))
        self.entropy = data[10]


class SaturatedSteam(SaturationLineWater):
    """Liquid water on saturated state."""

    name = "Saturated steam"

    def _set_state(self, property_state):
        """Set instance atributes for given state."""
        data = self._find_state(property_state)
        self.temperature = Celcius(data[0])
        self.pressure = KiloPascal(data[1])
        self.volume = CubicMeterPerKiloGram(data[3])
        self.energy = KJPerKg(data[6])
        self.enthalpy = SpecificEnthalpy(KJPerKg(data[9]))
        self.enthalpy_condensation = SpecificEnthalpy(KJPerKg(data[8]) * -1)
        self.entropy = data[12]
