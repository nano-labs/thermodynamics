#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Energy units."""

from units import GenericUnit

__all__ = ["KJPerKg"]
__dir__ = __all__


class SpecificEnergy(GenericUnit):
    """Abstraction of Specific energy."""

    property_name = "specific_energy"


class KJPerKg(SpecificEnergy):

    symbol = u"kJ/kg"

    def __init__(self, value):
        self.value = value
