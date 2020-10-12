from django.db import models
from index.models import Person


# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=100)
    body = models.TextField()
    author = models.ForeignKey(Person, on_delete=models.CASCADE)
    posted = models.DateTimeField()
