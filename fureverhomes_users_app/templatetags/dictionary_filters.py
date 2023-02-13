import django.templatetags
from django import template


def get_item(dictionary, key):
	return dictionary.get(key)