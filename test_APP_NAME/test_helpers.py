from django.template import TemplateDoesNotExist

from unittest import TestCase

from nose import tools


class TemplateLoader(object):
    def __init__(self):
        self.reset()
        self.base_templates = {}

    def reset(self):
        self.templates = {}

    def register(self, template_name, content='', one_time=True):
        self.templates[template_name] = (content, one_time)

    def register_builtin(self, template_name, content=''):
        self.base_templates[template_name] = content

    def load_template_source(self, template_name, dirs=None):
        "Dummy template loader that returns templates from local templates dictionary."
        try:
            (content, one_time) = self.templates[template_name]
            if one_time:
                del self.templates[template_name]
            return content, template_name
        except KeyError, e:
            if template_name in self.base_templates:
                return self.base_templates[template_name], template_name
            raise TemplateDoesNotExist(e)
    load_template_source.is_usable = True


loader = TemplateLoader()
load_template_source = loader.load_template_source


class TestDummyTemplateLoader(TestCase):
    def tearDown(self):
        loader.reset()

    def test_simple(self):
        loader.register('anything.html', 'Something')
        source, name = loader.load_template_source('anything.html')
        tools.assert_equals('anything.html', name)
        tools.assert_equals('Something', source)

    def test_empty(self):
        tools.assert_raises(TemplateDoesNotExist, loader.load_template_source, 'anything.html')

    def test_one_time(self):
        loader.register('anything.html', one_time=True)
        source, name = loader.load_template_source('anything.html')
        tools.assert_equals('anything.html', name)
        tools.assert_raises(TemplateDoesNotExist, loader.load_template_source, 'anything.html')

