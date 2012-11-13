from datetime import datetime

from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.generic import GenericForeignKey

class RComment(models.Model):
    content_type = models.ForeignKey(ContentType)
    object_pk = models.TextField()

    content_object = GenericForeignKey('content_type', 'object_pk')

    user = models.ForeignKey(User)
    submit_date = models.DateTimeField(db_index=True, default=datetime.now)
    text = models.TextField()
    moderated = models.BooleanField(default=False)

    def is_public(self):
        return self.submit_date <= datetime.now() and not self.moderated
