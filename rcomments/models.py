from datetime import datetime

from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.generic import GenericForeignKey

class RCommentManager(models.Manager):
    def for_model(self, obj):
        ct = ContentType.objects.get_for_model(obj)
        return self.filter(moderated=False, submit_date__lte=datetime.now(),
                content_type=ct, object_pk=obj.pk).order_by('-submit_date')

class RComment(models.Model):
    content_type = models.ForeignKey(ContentType)
    object_pk = models.TextField()

    content_object = GenericForeignKey('content_type', 'object_pk')

    user = models.ForeignKey(User)
    submit_date = models.DateTimeField(db_index=True, default=datetime.now)
    text = models.TextField()
    moderated = models.BooleanField(default=False)

    objects = RCommentManager()

    def is_public(self):
        return self.submit_date <= datetime.now() and not self.moderated

    def moderate(self, commit=True):
        self.moderated = True
        if commit:
            self.save(force_update=True)
