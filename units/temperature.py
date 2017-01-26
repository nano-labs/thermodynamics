#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Temperature units."""

from units import GenericUnit

__all__ = ["Celcius", "Kelvin", "Fahrenheit"]
__dir__ = __all__


class Temperature(GenericUnit):
    """Comparative measurement of hot or cold."""

    property_name = "temperature"

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


class Celcius(Temperature):
    """Temperature on Celcius degress."""

    symbol = u"°C"

    def __init__(self, value):
        """Create a temperature instance started by celcius degress."""
        if isinstance(value, Temperature):
            value = Kelvin(value.base_value).celcius.value
        self.base_value = value + 273.15
        self.value = float(value)


class Kelvin(Temperature):
    """Temperature on Kelvin degress."""

    symbol = u"°K"

    def __init__(self, value):
        """Create a temperature instance started by kelvin degress."""
        if isinstance(value, Temperature):
            value = value.base_value
        self.base_value = float(value)
        self.value = self.base_value


class Fahrenheit(Temperature):
    """Temperature on Fahrenheit degress."""

    symbol = u"°F"

    def __init__(self, value):
        """Create a temperature instance started by celcius degress."""
        if isinstance(value, Temperature):
            value = Kelvin(value.base_value).fahrenheit.value
        self.base_value = (value + 459.67) * 5/9.0
        self.value = float(value)
