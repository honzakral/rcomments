from datetime import datetime, timedelta
from unittest import TestCase

from rcomments.models import RComment

from nose import tools

class TestRComment(TestCase):
    def test_comment_in_future_arent_public(self):
        rc = RComment(submit_date=datetime.now() + timedelta(10))

        tools.assert_false(rc.is_public())

    def test_moderated_command_is_not_public(self):
        rc = RComment(submit_date=datetime.now() - timedelta(10), moderated=True)

        tools.assert_false(rc.is_public())


