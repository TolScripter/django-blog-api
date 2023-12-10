from django.db import models 
from django.contrib.auth.models import User

class Tag(models.Model):
    title = models.CharField(max_length=150)
    code = models.CharField(max_length=50)
    description = models.TextField()
    at = models.DateTimeField(auto_now=True)


    
class Category(models.Model):
    name = models.CharField(max_length=255)
    at = models.DateTimeField(auto_now=True)

    

class Post(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    img = models.ImageField(upload_to='../images')
    category = models.ManyToManyField(Category)
    tags = models.ManyToManyField(Tag)
    at = models.DateTimeField(auto_now=True)
    
    
class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    at = models.DateTimeField(auto_now=True)


class View(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    at = models.DateTimeField(auto_now=True)


class Collection(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    at = models.DateTimeField(auto_now=True)
