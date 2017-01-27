#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Conteiners for substances."""

from units.amount import Volume, Mass
from properties import Enthalpy


class UnsuportedOperation(Exception):
    """Cannot operate different substances or containers."""

    def __init__(self):
        """Set message to raise."""
        message = "Can operate equal substances or containers only."
        super(UnsuportedOperation, self).__init__(message)


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
        self.volume = (self.substance.volume * mass).liter
        self.energy = self.substance.energy * mass
        self.enthalpy = Enthalpy(self.substance.enthalpy * mass)

    def __unicode__(self):
        """Unicode representation."""
        return u"Flask with %s of %s" % (self.mass, self.substance)

    def __str__(self):
        """String representation."""
        return self.__unicode__().encode("utf-8")

    def __repr__(self):
        """Short representation."""
        return self.__str__()

    def __add__(self, added):
        """Add flasks of same substance."""
        if isinstance(added, self.__class__):
            if added.substance.__class__ == self.substance.__class__:
                total_mass = self.mass + added.mass
                total_enthalpy = self.enthalpy + added.enthalpy
                specific_enthalpy = total_enthalpy / total_mass
                new_substance = self.substance.__class__(specific_enthalpy)
                return Flask(new_substance, total_mass)
            else:
                raise UnsuportedOperation()
        else:
            raise UnsuportedOperation()
