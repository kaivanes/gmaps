import traitlets as traitlets

from . import utils


class CSSDimension(traitlets.TraitType):

    default_value = '0'
    info_text = 'A CSS dimension'

    def validate(self, obj, value):
        value = utils.parse_css_dimension(value)
        return value
