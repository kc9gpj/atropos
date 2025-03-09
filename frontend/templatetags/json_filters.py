from django import template
import json

register = template.Library()

@register.filter
def pprint(value):
    try:
        if isinstance(value, str):
            value = json.loads(value)
        return json.dumps(value, indent=2)
    except:
        return value