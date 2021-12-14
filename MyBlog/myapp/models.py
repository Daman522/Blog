from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models.deletion import CASCADE
# Create your models here.


class Post(models.Model):
    title=models.CharField(max_length=50)
    desc=models.TextField()
    date_posted=models.DateTimeField(default=timezone.now)
    author=models.ForeignKey(User,on_delete=CASCADE)
    image=models.ImageField(upload_to='images',blank=True,null=True)
    


    def __str__(self):
        return self.title