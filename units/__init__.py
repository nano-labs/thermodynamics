#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Abstraction of phisical properties and it's units."""


class UnitNotSuported(Exception):
    pass


class UndefinedUnit(Exception):
    pass


class UnitMismatch(Exception):
    pass


class UnlogicalOperation(Exception):
    """Does not make sense to mathematicaly operate different properties."""

    def __init__(self, operand_a, operand_b):
        """Set message to raise."""
        message = "Cannot operate different phisical properties: %s and %s" % (
                   type(operand_a), type(operand_b))
        super(UnlogicalOperation, self).__init__(message)


class GenericUnit(object):
    """Every unit must extend this object."""

    # Unit value
    value = None
    base_value = None
    symbol = u""
    property_name = ""

    def __init__(self, *args, **kwargs):
        """Can't instance."""
        raise UnitNotSuported("Cannot instance %s directly." % self.__class__)

    def __unicode__(self):
        """Unicode representation."""
        if self.value >= 0.01:
            return u"%.2f %s" % (self.value, self.symbol)
        return u"%f %s" % (self.value, self.symbol)

    def __str__(self):
        """String representation."""
        return self.__unicode__().encode("utf-8")

    def __repr__(self):
        """Short representation."""
        return self.__str__()

    def __int__(self):
        """Method used by int() function."""
        return int(self.value)

    def __float__(self):
        """Method used by float() function."""
        return float(self.value)

    def __mul__(self, multiplier):
        """Multiply method."""
        return self.__class__(self.value * multiplier)

    def __imul__(self, multiplier):
        """Multiply method."""
        self = self * multiplier
        return self

    def __div__(self, divisor):
        """Division method."""
        return self.__class__(self.value / float(divisor))

    def __idiv__(self, divisor):
        """Division method."""
        self = self / float(divisor)
        return self

    def __add__(self, added):
        """Addition method."""
        if self.issameproperty(added):
            return self.__class__(self.value + self.__class__(added).value)
        elif isinstance(added, float) or isinstance(added, int):
            return self.__class__(self.value + added)
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

    def issameproperty(self, other):
        """Check if this unit is the same kind of property as other one."""
        try:
            return self.property_name == other.property_name
        except AttributeError:
            return False
