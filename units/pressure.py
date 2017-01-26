#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Pressure units."""

from units import GenericUnit

__all__ = ["Pascal", "KiloPascal", "Atmosphere", "Bar", "PSI",
           "PoundSquareInch"]
__dir__ = __all__


class Pressure(GenericUnit):
    """Abstraction of pressure units."""

    property_name = "pressure"

    @property
    def pascal(self):
        """Pressure using Pascals."""
        return Pascal(self.base_value)

    @property
    def bar(self):
        """Pressure using Bar."""
        return Bar(self.base_value / 100000.0)

    @property
    def atmosphere(self):
        """Pressure using Atmosferes."""
        return Atmosphere(self.base_value / 101325.0)

    @property
    def kPa(self):
        """Pressure using Kilo Pascal."""
        return KiloPascal(self.base_value / 1000.0)

    @property
    def psi(self):
        """Pressure using Pound per square inch."""
        return PoundSquareInch(self.base_value / 6894.76)

    @property
    def kilo_pascal(self):
        """Pressure using Kilo Pascal."""
        return self.kPa


class Pascal(Pressure):
    """Pascal unit."""

    symbol = u"Pa"

    def __init__(self, value):
        """Create a pressure instance started by Pascals."""
        if isinstance(value, Pressure):
            value = value.base_value
        self.base_value = float(value)
        self.value = self.base_value


class KiloPascal(Pressure):
    """Kilo Pascal unit."""

    symbol = u"kPa"

    def __init__(self, value):
        """Create a pressure instance started by Pascals."""
        if isinstance(value, Pressure):
            value = Pascal(value.base_value).kPa.value
        self.base_value = value * 1000.0
        self.value = float(value)


class Bar(Pressure):
    """Bar unit."""

    symbol = u"bar"

    def __init__(self, value):
        """Create a pressure instance started by Bars."""
        if isinstance(value, Pressure):
            value = Pascal(value.base_value).bar.value
        self.base_value = value * 100000.0
        self.value = float(value)


class Atmosphere(Pressure):
    """Atmosfere unit."""

    symbol = u"atm"

    def __init__(self, value):
        """Create a pressure instance started by atms."""
        if isinstance(value, Pressure):
            value = Pascal(value.base_value).atmosphere.value
        self.base_value = value * 101325.0
        self.value = float(value)


class PoundSquareInch(Pressure):
    """Pound per Square inch unit."""

    symbol = u"psi"

    def __init__(self, value):
        """Create a pressure instance started by psi."""
        if isinstance(value, Pressure):
            value = Pascal(value.base_value).psi.value
        self.base_value = value * 6894.76
        self.value = float(value)


class PSI(PoundSquareInch):
    """Alias for PoundSquareInch."""

    pass
