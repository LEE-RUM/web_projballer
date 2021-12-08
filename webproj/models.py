from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Forum(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post_title = models.CharField(max_length=200)
    post = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return self.post_title

class Comment(models.Model):

    post = models.ForeignKey(Forum,on_delete=models.CASCADE,related_name='comments')
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)



