from django.test import RequestFactory
from django.http import Http404

from rcomments.views import comment_list

from nose import tools

from test_rcomments.cases import RCommentTestCase

class TestCommentList(RCommentTestCase):
    def setUp(self):
        super(TestCommentList, self).setUp()
        self.comments = [self._create_comment(text='%dth' % x) for x in xrange(2)]
        self.rf = RequestFactory()
        self.request = self.rf.get('/')

    def test_404_raised_on_non_existent_content_type(self):
        tools.assert_raises(Http404, comment_list, self.request, '234455', '1')

    def test_404_raised_on_non_existent_object(self):
        tools.assert_raises(Http404, comment_list, self.request, str(self.ct.pk), '234455')

    def test_comment_list_renders_template_with_proper_queryest(self):
        response = comment_list(self.request, str(self.ct.pk), str(self.ct.pk))

        tools.assert_in('comment_list', response.context_data)
        tools.assert_equals(set(c.pk for c in self.comments), set(c.pk for c in response.context_data['comment_list']))

