from django import template

register = template.Library()

@register.filter(name='entry_title')
def entry_title_filter(s):
    if not s.startswith("guardian scout"):
        return s.title()
    else:
        parts = s.split(" ")
        return f"{parts[0].title()} {parts[1].title()} {parts[2].upper()}"