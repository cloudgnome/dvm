from django.forms import TextInput
from django.utils.safestring import mark_safe
from django.template.loader import render_to_string

__all__ = ['CategoryWidget']

class CategoryWidget(TextInput):
    template_name = "catalog/categories.html"

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        return context

    def render(self, *args, **kwargs):
        return mark_safe(render_to_string(self.template_name))