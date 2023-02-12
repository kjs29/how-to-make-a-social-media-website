from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
# Create your models here.

class Post(models.Model):
    title = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField()
    photo = models.ImageField(null=True, blank=True)
    original_filename = models.CharField(max_length=255, null=True, blank=True)
    likes = models.ManyToManyField(User, related_name="blog_post", blank=True)
    created_date = models.DateTimeField(auto_now_add=timezone.now)

    def __str__(self):
        return f"{self.title} | {self.user}"

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name="Post this comment is on")
    body = models.TextField()
    created_date = models.DateTimeField(auto_now=timezone.now)
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="commented by")

    def __str__(self):
        return f"{self.body[:25]} on {self.post} by {self.user}"