#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Energy units."""

from units import UnitMismatch, UnlogicalOperation, UnitNotSupported, GenericUnit
from units.amount import Mass
from units.energy import Energy, SpecificEnergy

__all__ = ["Enthalpy"]
__dir__ = __all__


class GenericProperty(object):
    """Base model for properties"""

    property_name = ""
    _base_unit = None

    def __init__(self, *args, **kwargs):
        """Can't instance."""
        raise UnitNotSupported("Cannot instance Property directly.")

    def __unicode__(self):
        """Unicode representation."""
        return u"%s (%s)" % (self._base_unit, self.property_name)

    def __str__(self):
        """String representation."""
        return self.__unicode__().encode("utf-8")

    def __repr__(self):
        """Short representation."""
        return self.__str__()

    def __int__(self):
        """Method used by int() function."""
        return int(self._base_unit.value)

    def __float__(self):
        """Method used by float() function."""
        return float(self._base_unit.value)

    def __mul__(self, multiplier):
        """Multiply method."""
        return self.__class__(self._base_unit * multiplier)

    def __imul__(self, multiplier):
        """Multiply method."""
        self = self * multiplier
        return self

    def __div__(self, divisor):
        """Division method."""
        return self.__class__(self._base_unit / float(divisor))

    def __idiv__(self, divisor):
        """Division method."""
        self = self / float(divisor)
        return self

    def __add__(self, added):
        """Addition method."""
        if isinstance(added, self.__class__):
            return self.__class__(self._base_unit + added._base_unit)
        elif isinstance(added, self._base_unit.__class__):
            return self.__class__(self._base_unit + added)
        elif isinstance(added, float) or isinstance(added, int):
            return self.__class__(self._base_unit + added)
        else:
            raise UnlogicalOperation(self, added)

    def __iadd__(self, added):
        """Addition method."""
        self = self + added
        return self

    def __sub__(self, subtractor):
        """Subtraction method."""
        return self + (subtractor * -1)

    def __isub__(self, subtractor):
        """Subtraction method."""
        self = self - subtractor
        return self


class Enthalpy(GenericProperty):
    """Defines the enthalpy property of the system."""

    property_name = "enthalpy"

    def __init__(self, energy):
        """It is basicaly a measurement of energy."""
        if not isinstance(energy, Energy):
            raise UnitMismatch("Energy instance is needed")
        self._base_unit = energy

    @property
    def energy(self):
        """Semantic alias for _base_unit."""
        return self._base_unit

    def __div__(self, divisor):
        """Division method."""
        if isinstance(divisor, Mass):
            return SpecificEnthalpy(self._base_unit / divisor)
        return super(self.__class__, self).__div__(divisor)


class SpecificEnthalpy(GenericProperty):
    """Defines the specific enthalpy property of a substance."""

    property_name = "specific enthalpy"

    def __init__(self, specific_energy):
        """It is basicaly a measurement of energy rate of a substance."""
        if not isinstance(specific_energy, SpecificEnergy):
            raise UnitMismatch("SpecificEnergy instance is needed")
        self._base_unit = specific_energy

    @property
    def specific_energy(self):
        """Semantic alias for _base_unit."""
        return self._base_unit

    def __mul__(self, multiplier):
        """Multiply method."""
        result = self._base_unit * multiplier
        if isinstance(result, GenericUnit):
            return result
        return self.__class__(result)
