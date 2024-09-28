from django import template

register = template.Library()


@register.filter(name='mult')
def mult(value, arg):
    """
        :param value: The first value to be multiplied.
        :param arg: The second value to multiply with the first.
        :return: The product of the two values.
    """

    return value * arg


@register.filter(name='div')
def div(value, arg):
    """
        :param value: The numerator in the division operation.
        :param arg: The denominator in the division operation.
        :return: The result of dividing value by arg.
    """

    return value / arg
