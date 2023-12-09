from django.db import models 
from django.contrib.auth.models import User

class Tag(models.Model):
    title = models.CharField(max_length=150)
    code = models.CharField(max_length=50)
    description = models.TextField()
    at = models.DateTimeField(auto_now=True)


    def __str__(self) -> str:
        return self.code
    
class Category(models.Model):
    name = models.CharField(max_length=255)
    at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.name
    

class Post(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    img = models.ImageField(upload_to='../images')
    category = models.ManyToManyField(Category)
    tags = models.ManyToManyField(Tag)
    at = models.DateTimeField(auto_now=True)
    
    def __str__(self) -> str:
        return self.title
    
class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.at
    

class View(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.at


class Collection(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.at
