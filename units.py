#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Abstraction of phisical properties and it's units."""


class UnitNotSuported(Exception):
    pass


class UndefinedUnit(Exception):
    pass


class UnlogicalOperation(Exception):

    def __init__(self, operand_a, operand_b):
        message = "Cannot operate different phisical properties: %s and %s" % (
                   type(operand_a), type(operand_b))
        super(UnlogicalOperation, self).__init__(message)


class GenericUnit(object):

    # Unit value
    value = None
    symbol = ""

    def __unicode__(self):
        """Unicode representation."""
        return "%.2f %s" % (self.value, self.symbol)

    def __str__(self):
        """String representation."""
        return str(self.__unicode__())

    def __repr__(self):
        """Short representation."""
        return self.__str__()

    def __int__(self):
        """Method used by int() function."""
        return int(self.value)

    def __float__(self):
        """Method used by float() function."""
        return float(self.value)


class Temperature(GenericUnit):
    """Comparative measurement of hot or cold."""

    # SI value of the property. Used for standardization and math
    base_value = None  # kelvin

    def __init__(self, *args, **kwargs):
        """Can't instance a Temperature."""
        raise UnitNotSuported("Cannot instance Temperature directly.")

    @property
    def kelvin(self):
        """Temperature using Kelvin scale."""
        return Kelvin(self.base_value)

    @property
    def celcius(self):
        """Temperature using Celcius scale."""
        return Celcius(self.base_value - 273.15)

    @property
    def fahrenheit(self):
        """Temperature using Fahrenheit scale."""
        return Fahrenheit((self.base_value * (9/5.0)) - 459.67)


    def __add__(self, added):
        """Addition method."""
        if isinstance(added, Temperature):
            return self.__class__(self.value + self.__class__(added).value)
        elif isinstance(added, float) or isinstance(added, int):
            return self.__class__(self.value + added)
        else:
            raise UnlogicalOperation(self, added)


class Celcius(Temperature):
    """Temperature on Celcius degress."""

    symbol = "°C"

    def __init__(self, value):
        """Create a temperature instance started by celcius degress."""
        if isinstance(value, Temperature):
            value = Kelvin(value.base_value).celcius
        self.base_value = value + 273.15
        self.value = float(value)


class Kelvin(Temperature):
    """Temperature on Kelvin degress."""

    symbol = "°K"

    def __init__(self, value):
        """Create a temperature instance started by kelvin degress."""
        if isinstance(value, Temperature):
            value = value.base_value
        self.base_value = float(value)
        self.value = self.base_value


class Fahrenheit(Temperature):
    """Temperature on Fahrenheit degress."""

    symbol = "°F"

    def __init__(self, value):
        """Create a temperature instance started by celcius degress."""
        if isinstance(value, Temperature):
            value = Kelvin(value.base_value).fahrenheit
        self.base_value = (value + 459.67) * 5/9.0
        self.value = float(value)


class SpecificEnergy(GenericUnit):
    """Abstraction of Specific energy."""
    pass


class KJPerKg(SpecificEnergy):

    symbol = "kJ/kg"

    def __init__(self, value):
        self.value = value
