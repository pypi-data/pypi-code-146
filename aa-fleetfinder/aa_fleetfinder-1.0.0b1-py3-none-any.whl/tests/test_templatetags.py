"""
Test the apps' template tags
"""

# Django
from django.template import Context, Template
from django.test import TestCase

# AA Fleet Finder
from fleetfinder import __version__


class TestVersionedStatic(TestCase):
    """
    Test the fleetfinder_versioned_static template tag
    """

    def test_versioned_static(self):
        """
        Test should return a versioned static
        :return:
        :rtype:
        """

        context = Context({"version": __version__})
        template_to_render = Template(
            "{% load fleetfinder_versioned_static %}"
            "{% fleetfinder_static 'fleetfinder/css/fleetfinder.min.css' %}"
        )

        rendered_template = template_to_render.render(context)

        self.assertInHTML(
            f'/static/fleetfinder/css/fleetfinder.min.css?v={context["version"]}',
            rendered_template,
        )
