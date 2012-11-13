from datetime import datetime, timedelta
from unittest import TestCase

from rcomments.models import RComment

from nose import tools

from test_rcomments.cases import RCommentTestCase

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

class TestRCommentWithDB(RCommentTestCase):
    def test_moderate_saves_comment(self):
        rc = self._create_comment()
        rc.moderate()

        rc = RComment.objects.get(pk=rc.pk)
        tools.assert_true(rc.moderated)

    def test_manager_returns_comments_for_proper_object(self):
        rc = self._create_comment()
        self._create_comment(content_object=rc)

        clist = RComment.objects.for_model(self.ct)

        tools.assert_equals(1, clist.count())
        tools.assert_equals(rc, clist[0])

    def test_manager_ommits_moderated_comments(self):
        self._create_comment(moderated=True)

        clist = RComment.objects.for_model(self.ct)

        tools.assert_equals(0, clist.count())

    def test_manager_ommits_comments_in_future(self):
        self._create_comment(submit_date=datetime.now() + timedelta(10))

        clist = RComment.objects.for_model(self.ct)

        tools.assert_equals(0, clist.count())
