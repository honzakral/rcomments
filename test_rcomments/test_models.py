from datetime import datetime, timedelta
from unittest import TestCase

from django.test import TestCase as DjangoTestCase
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User

from rcomments.models import RComment

from nose import tools

class TestRComment(TestCase):
    def test_comment_in_future_arent_public(self):
        rc = RComment(submit_date=datetime.now() + timedelta(10))

        tools.assert_false(rc.is_public())

    def test_moderated_command_is_not_public(self):
        rc = RComment(submit_date=datetime.now() - timedelta(10), moderated=True)

        tools.assert_false(rc.is_public())


    def test_moderate_comment_sets_moderated_flag(self):
        rc = RComment()
        rc.moderate(False)

        tools.assert_true(rc.moderated)

class TestRCommentWithDB(DjangoTestCase):
    def setUp(self):
        super(TestRCommentWithDB, self).setUp()
        self.ct = ContentType.objects.get_for_model(ContentType)
        self.user = User.objects.create_user('some-user', 'user@example.com')

    def _create_comment(self, **kwargs):
        defaults = dict(content_object=self.ct, user=self.user, text='First!')
        defaults.update(kwargs)
        return RComment.objects.create(**defaults)

    def test_moderate_saves_comment(self):
        rc = self._create_comment()
        rc.moderate()

        rc = RComment.objects.get(pk=rc.pk)
        tools.assert_true(rc.moderated)
