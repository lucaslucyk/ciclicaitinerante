from __future__ import unicode_literals


from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse

from django.conf import settings

# Create your models here.
#from posts.models import Post

class CommentManager(models.Manager):
    def all(self):
        qs = super(CommentManager, self).filter(parent=None)
        return qs
    def filter_by_instance(self, instance):
        content_type = ContentType.objects.get_for_model(instance.__class__)
        obj_id = instance.id
        qs = super(CommentManager, self).filter(content_type=content_type, object_id=obj_id).filter(parent=None)
        return qs

class Comment(models.Model):
    user        = models.ForeignKey(settings.AUTH_USER_MODEL, default=1, null=True, on_delete=models.SET_NULL)
    #post        = models.ForeignKey(Post, on_delete=models.SET_NULL, null=True)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    parent = models.ForeignKey("self", null=True, blank=True, on_delete=models.CASCADE)

    content     = models.TextField()
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

    objects = CommentManager()

    class Meta:
        ordering = ['-timestamp']

    def __unicode__(self):
        return str(self.user.username)
    def __str__(self):
        return str(self.user.username)

    def get_absolute_url(self):
        return reverse("comments:comment_thread", kwargs={"id": self.id})

    def children(self): #replies
        return Comment.objects.filter(parent=self)

    @property
    def is_parent():
        if self.parent is not None:
            return False
        return True