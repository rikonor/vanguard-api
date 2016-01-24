class ValueConvertionFailure(Exception):
    pass

class Converters(object):
    @staticmethod
    def sanitize_unicode_signs(val):
        return val.replace(u'\u2013', '-')

    @staticmethod
    def percent(v):
        # Sanitize input (spaces, commas)
        val = Converters.sanitize_unicode_signs(v)
        val = val.replace(' ', '').replace(',', '')

        if "%" not in val:
            raise ValueConvertionFailure("No percent symbol found: {}".format(v))

        # Remove percent symbol (assuming it's at the end)
        if val[-1] != "%":
            raise ValueConvertionFailure("Percent symbol should be at end of string: {}".format(v))
        val = val[:-1]

        try:
            percent = float(val)
        except ValueError:
            raise ValueConvertionFailure("Failed percent conversion: {}".format(v))

        return percent / 100

    @staticmethod
    def dollar_amount(v):
        # Sanitize input (spaces, commas and dollar symbol)
        val = Converters.sanitize_unicode_signs(v)
        val = val.replace(' ', '').replace(',', '').replace('$', '')

        try:
            dollar_amount = float(val)
        except ValueError:
            raise ValueConvertionFailure("Failed dollar amount conversion: {}".format(v))

        return dollar_amount
