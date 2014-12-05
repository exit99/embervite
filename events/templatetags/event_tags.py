from django import template

from embervite.constants import WEEK_DAYS

register = template.Library()


@register.filter
def week_day(num):
    return WEEK_DAYS.get(int(num), "Error")
