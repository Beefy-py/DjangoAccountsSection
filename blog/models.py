from django.db import models
from django.urls import reverse
from django.contrib.auth import get_user_model


# Create your models here.
class Post(models.Model):
    class Meta:
        ordering = ['-posted']

    title = models.CharField(max_length=100)
    header_image = models.ImageField(null=True, blank=True, upload_to='images/')
    body = models.TextField()
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    posted = models.DateTimeField(auto_now_add=True)
    last_edited = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title[:20]

    def get_absolute_url(self):
        return reverse('post_list')
