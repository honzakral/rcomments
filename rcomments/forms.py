from django.forms.models import ModelForm

from rcomments.models import RComment

class RCommentForm(ModelForm):
    def __init__(self, obj, user, *args, **kwargs):
        self.obj = obj
        self.user = user
        super(RCommentForm, self).__init__(*args, **kwargs)

    def clean(self):
        self.instance.user = self.user
        self.instance.content_object = self.obj
        return super(RCommentForm, self).clean()

    class Meta:
        model = RComment
        fields = ('text', )
