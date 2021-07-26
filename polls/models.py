from django.db import models

# Create your models here.
from django.db import models


class Blog(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name


class Author(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()

    def __str__(self):
        return self.name


class Post(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    pub_date = models.DateField(auto_now_add=True)
    mod_date = models.DateField(auto_now=True)
    authors = models.ManyToManyField(Author)
    number_of_comments = models.IntegerField(default=0)
    number_of_likes = models.IntegerField(default=0)
    rating = models.IntegerField(null=True, blank=True, default=None)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-pub_date', '-number_of_likes']
