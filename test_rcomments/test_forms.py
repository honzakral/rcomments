from unittest import TestCase

from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User

from rcomments.forms import RCommentForm

from nose import tools

class TestRCommentForm(TestCase):
    def setUp(self):
        super(TestRCommentForm, self).setUp()
        self.ct = ContentType.objects.get_for_model(ContentType)
        self.user = User(username='some-user', email='user@example.com')

    def test_comment_from_comment_form_is_complete(self):
        form = RCommentForm(self.ct, self.user, {'text': 'Heya!'})

        tools.assert_true(form.is_valid())
        rc = form.save(commit=False)
        tools.assert_equals(self.user, rc.user)
        tools.assert_equals(self.ct.pk, rc.content_type_id)
        tools.assert_equals('Heya!', rc.text)
        tools.assert_true(rc.is_public())
