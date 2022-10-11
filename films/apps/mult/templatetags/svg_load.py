import xml.etree.ElementTree as ET

from django import template
from django.utils.safestring import mark_safe
from django.conf import settings
from os.path import join
from django.template import Context
from django.template.loader import get_template
from django.template.loader_tags import BlockNode, ExtendsNode

register = template.Library()

ICON_DIR = join(settings.STATIC_ROOT, "mult", "image")


@register.simple_tag
def icon(file_name, class_str=None, size=24, fill='#000000'):
    """Inlines a SVG icon from assets/mult/image

    Example usage:
        {% icon 'face' 'std-icon menu-icon' 32 '#ff0000' %}
    Parameter: file_name
        Name of the icon file excluded the .svg extention.
    Parameter: class_str
        Adds these class names, use "foo bar" to add multiple class names.
    Parameter: size
        An integer value that is applied in pixels as the width and height to
        the root element.
        The material.io icons are by default 24px x 24px.
    Parameter: fill
        Sets the fill color of the root element.
    Returns:
        XML to be inlined, i.e.:
        <svg width="..." height="..." fill="...">...</svg>
    """
    # path = f'{ICON_DIR}/{file_name}.svg'
    path = join(ICON_DIR, file_name+'.svg')
    ET.register_namespace('', "http://www.w3.org/2000/svg")
    tree = ET.parse(path)
    root = tree.getroot()
    root.set('class', class_str)
    root.set('width', f'{size}px')
    root.set('height', f'{size}px')
    root.set('fill', fill)
    svg = ET.tostring(root, encoding="unicode", method="html")
    return mark_safe(svg)


@register.tag
def include_block(parser, token):
    try:
        tag_name, include_file, block_name = token.split_contents()
        include_file = f"{settings.PROJECT_ROOT}/templates/{include_file}"
    except ValueError:
        raise template.TemplateSyntaxError("%r tag requires a two arguments" % (token.contents.split()[0]))
    return IncludeBlockNode(include_file.replace('"', ''), block_name.replace('"', ''))


class IncludeBlockNode(template.Node):
    def __init__(self, include_file, block_name):
        self.include_file = include_file
        self.block_name = block_name

    def _get_node(self, template, context, name):
        if hasattr(template, 'template'):
            for node in template.template:
                if isinstance(node, BlockNode) and node.name == name:
                    return node.render(Context(context))
                elif isinstance(node, ExtendsNode):
                    return self._get_node(node.nodelist, context, name)
        else:
            for node in template:
                if isinstance(node, BlockNode) and node.name == name:
                    return node.render(Context(context))
                elif isinstance(node, ExtendsNode):
                    return self._get_node(node.nodelist, context, name)
        raise Exception("Node '%s' could not be found in template." % name)

    def render(self, context):
        t = get_template(self.include_file)
        return self._get_node(t, context, self.block_name)
