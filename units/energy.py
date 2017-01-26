#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Energy units."""

from units import GenericUnit
from units.amount import Mass, KiloGram

__all__ = ["KJPerKg"]
__dir__ = __all__


class SpecificEnergy(GenericUnit):
    """Abstraction of Specific energy."""

    def __mul__(self, multiplier):
        """Specific volume versus mass equals volume."""
        if isinstance(multiplier, Mass):
            return KiloJoule(KiloGram(multiplier).value * self.base_value)
        else:
            return super(SpecificEnergy, self).__mul__(multiplier)

    property_name = "specific_energy"


class KJPerKg(SpecificEnergy):

    symbol = u"kJ/kg"

    def __init__(self, value):
        """Create a specific energy instance started by kJ/kg."""
        if isinstance(value, SpecificEnergy):
            value = value.base_value
        self.base_value = float(value)
        self.value = self.base_value


class Energy(GenericUnit):
    """Abstraction of energy."""

    property_name = "energy"

    @property
    def joule(self):
        """Energy using Joules."""
        return Joule(self.base_value)

    @property
    def kJ(self):
        """Energy using Kilo Joules."""
        return KiloJoule(self.base_value / 1000.0)


class Joule(Energy):

    symbol = u"J"

    def __init__(self, value):
        """Create a energy instance started by Joules."""
        if isinstance(value, Energy):
            value = value.base_value
        self.base_value = float(value)
        self.value = self.base_value


class KiloJoule(Energy):

    symbol = u"kJ"

    def __init__(self, value):
        """Create a energy instance started by kiloJoules."""
        if isinstance(value, Energy):
            value = Joule(value.base_value).kPa.value
        self.base_value = value * 1000.0
        self.value = float(value)
