from django.test import TestCase
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User

from rcomments.models import RComment

class RCommentTestCase(TestCase):
    def setUp(self):
        super(RCommentTestCase, self).setUp()
        self.ct = ContentType.objects.get_for_model(ContentType)
        self.user = User.objects.create_user('some-user', 'user@example.com')

    def _create_comment(self, **kwargs):
        defaults = dict(content_object=self.ct, user=self.user, text='First!')
        defaults.update(kwargs)
        return RComment.objects.create(**defaults)

