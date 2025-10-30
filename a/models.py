from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=500)
    description = models.TextField()
    img = models.ImageField(upload_to="images/",null=True,blank=True)
    vid = models.FileField(upload_to="videos/",null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    edited_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User,on_delete=models.CASCADE)

class Like(models.Model):
    post = models.ForeignKey(Post,on_delete=models.CASCADE,related_name="likes")
    author = models.ForeignKey(User,on_delete=models.CASCADE,related_name="likes")
    class Meta:
        unique_together = ('post','author')

class Dislike(models.Model):
    post = models.ForeignKey(Post,on_delete=models.CASCADE,related_name="dislikes")
    author = models.ForeignKey(User,on_delete=models.CASCADE,related_name="dislikes")
    class Meta:
        unique_together = ('post','author')

class Comment(models.Model):
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey(Post,on_delete=models.CASCADE,related_name="comments")
    author = models.ForeignKey(User,on_delete=models.CASCADE,related_name="comments")
