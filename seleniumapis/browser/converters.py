#!/usr/bin/env python
# -*- coding: utf-8 -*-

from enum import Enum

class ValueConversionFailure(Exception):
    pass

class TextType(Enum):
    plain,percent,dollar = range(3)

class Converters(object):
    @staticmethod
    def convert(v,textType):
        if textType == TextType.percent:
            return Converters.percent(v)
        elif textType == TextType.dollar:
            return Converters.dollar_amount(v)
        elif textType == TextType.plain:
            return Converters.plain(v)
        else:
            raise ValueConvertionFailure("Unknown TextType")

    @staticmethod
    def sanitize_unicode_signs(text,option=""):
        new_text = ""
        if option == "number":
            for char in text:
                if char.isdigit() or char == "." or char == "%":
                    new_text += char
                elif char == u'\u2013':
                    new_text += "-"
                else:
                    new_text += ""
        else:
            for char in text:
                if ord(char) >= 32 and ord(char) <= 126:
                    new_text += char
                elif char == u'\u2013':
                    new_text += "-"
                else:
                    new_text += ""

        return new_text

    @staticmethod
    def percent(v):
        # Sanitize input (spaces, commas)
        val = Converters.sanitize_unicode_signs(v,"number")

        if val == "":
            return None
        elif "%" not in val:
            raise ValueConversionFailure("No percent symbol found: {}".format(val))
        elif val[-1] != "%":
            raise ValueConversionFailure("Percent symbol should be at end of string: {}".format(val))
        else:
            val = val[:-1]

        try:
            percent = float(val)
        except ValueError:
            raise ValueConversionFailure("Failed percent conversion: {}".format(val))

        return percent / 100

    @staticmethod
    def dollar_amount(v):

        # When dollar amount is not available, a `-` is shown
        if u'—' == v:
            return 0.0

        # Sanitize input (spaces, commas and dollar symbol)
        val = Converters.sanitize_unicode_signs(v,"number")

        try:
            dollar_amount = float(val)
        except ValueError:
            raise ValueConversionFailure("Failed dollar amount conversion: {}".format(val))

        return dollar_amount

    @staticmethod
    def plain(v):
        val = Converters.sanitize_unicode_signs(v)

        return val.strip()
