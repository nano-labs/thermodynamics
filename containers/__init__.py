#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Conteiners for substances."""

from units.amount import Volume, Mass


class Flask(object):
    """Regular container with no special features."""

    substance = None
    mass = None
    volume = None
    energy = None
    enthalpy = None

    def __init__(self, substance, amount):
        """Fill the flask with given amount of substance."""
        self.substance = substance
        if isinstance(amount, Volume):
            self._update_by_volume(amount)
            self._update_by_mass(self.mass)
        elif isinstance(amount, Mass):
            self._update_by_mass(amount)

    def _update_by_volume(self, volume):
        """Update all attributes due volume changes."""
        self.volume = volume
        self.mass = volume / self.substance.volume

    def _update_by_mass(self, mass):
        """Update all attributes due volume changes."""
        self.mass = mass
        self.volume = self.substance.volume * mass
        self.energy = self.substance.energy * mass
        self.enthalpy = self.substance.enthalpy * mass
