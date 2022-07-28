from django import template
register = template.Library()

@register.filter(name="divide")
def divide(numerator, divisor):
    return float(numerator / divisor)

@register.filter(name="multiply")
def multiply(num1, num2):
    return float(num1 * num2)

