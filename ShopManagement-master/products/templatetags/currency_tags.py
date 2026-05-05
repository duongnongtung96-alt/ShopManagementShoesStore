from django import template

register = template.Library()

@register.filter(is_safe=False)
def vnd(value):
    """Format a numeric value as Vietnamese Dong with thousands separators."""
    if value is None:
        return ""

    try:
        amount = int(value)
    except (ValueError, TypeError):
        try:
            amount = float(value)
        except (ValueError, TypeError):
            return value

    return f"{amount:,.0f} VND"
