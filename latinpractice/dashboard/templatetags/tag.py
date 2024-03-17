from django import template

register = template.Library()

@register.simple_tag(takes_context=True)
def get_if_key_active(context):
    user = context['request'].user
    if user.profile.key_is_active:
        return ""
    else:
        return "disabled"