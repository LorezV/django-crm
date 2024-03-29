from django import template
import humanize

register = template.Library()


@register.simple_tag(takes_context=True)
def param_replace(context, **kwargs):
    d = context['request'].GET.copy()
    for k, v in kwargs.items():
        d[k] = v
    for k in [k for k, v in d.items() if not v]:
        del d[k]
    return d.urlencode()


@register.filter(name='makelist')
def makelist(number):
    return range(1, number+1)

@register.filter(name='humanize_int')
def humanize_int(number):
    return humanize.intcomma(number)


@register.filter(name='humanize_datetime')
def humanize_datetime(date):
    humanize.i18n.activate("ru_RU")
    return humanize.naturaldate(date)