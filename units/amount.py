#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Amount units."""

from units import GenericUnit

__all__ = []
__dir__ = __all__


class SpecificVolume(GenericUnit):
    """Abstraction of specific volume units."""

    property_name = "specific_volume"

    def __mul__(self, multiplier):
        """Specific volume versus mass equals volume."""
        if isinstance(multiplier, Mass):
            return CubicMeter(KiloGram(multiplier).value * self.base_value)
        else:
            return super(SpecificVolume, self).__mul__(multiplier)

    @property
    def m3_per_kg(self):
        """Pressure using Pascals."""
        return CubicMeterPerKiloGram(self.base_value)


class CubicMeterPerKiloGram(SpecificVolume):
    """Cubic meter per kilogram unit."""

    symbol = u"m³/kg"

    def __init__(self, value):
        u"""Create a specific volume instance started by m³/kg."""
        if isinstance(value, SpecificVolume):
            value = value.base_value
        self.base_value = float(value)
        self.value = self.base_value


class Volume(GenericUnit):
    """Abstraction of volume units."""

    property_name = "volume"

    def __div__(self, divisor):
        """Division by specific volume results mass."""
        if isinstance(divisor, SpecificVolume):
            return KiloGram(self.base_value / CubicMeterPerKiloGram(divisor).value)
        else:
            return super(Volume, self).__mul__(divisor)

    @property
    def m3(self):
        """Pressure using Pascals."""
        return CubicMeter(self.base_value)


class CubicMeter(Volume):
    """Cubic meter unit."""

    symbol = u"m³"

    def __init__(self, value):
        """Create a volume instance started by cubic meters."""
        if isinstance(value, Volume):
            value = value.base_value
        self.base_value = float(value)
        self.value = self.base_value


class Mass(GenericUnit):
    """Abstraction of mass units."""

    property_name = "mass"

    @property
    def kilogram(self):
        """Pressure using Pascals."""
        return KiloGram(self.base_value)


class KiloGram(Mass):
    """Kilogram unit."""

    symbol = u"kg"

    def __init__(self, value):
        """Create a mass instance started by kilograms."""
        if isinstance(value, Mass):
            value = value.base_value
        self.base_value = float(value)
        self.value = self.base_value
