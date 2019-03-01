import os
import yaml
from django import template

register = template.Library()


@register.filter(name="get_device_name")
def get_device_name(device):
    return get_lang("vocaburaly", device)


@register.filter(name="get_pin_title")
def get_pin_title(key):
    actions = get_lang("actions", "pins")
    return actions[int(key)]


@register.filter(name="get_lang")
def get_lang(_from, _key):
    with open(os.path.join("./app/lang", _from + ".yml")) as stream:
        try:
            config = yaml.load(stream)
            return config.get(_key)

        except yaml.YAMLError as exc:
            print(exc)
    return None
